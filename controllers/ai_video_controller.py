from flask import Blueprint, send_file, request, jsonify
from werkzeug.utils import secure_filename
import os
from services.extraction_invoice.main import process_invoices
from extensions import db
from models.bulk_invoice_status import BulkInvoiceStatus
from models.invoice import Invoice
import asyncio
from sqlalchemy.orm import selectinload
from services.ai_video.video import generate_video_prompt, download_video_content
from pprint import pprint

ai_video_handler = Blueprint("ai_video", __name__)
ai_video_callback_handler = Blueprint("ai_video_callback", __name__)

@ai_video_handler.route("/ai/video-prompt", methods=["POST"])
def ai_video_prompt():
    data = request.get_json()
    if not data or "prompt" not in data:
        return jsonify({"error": "No prompt provided"}), 400

    prompt = data["prompt"]
    seconds = data.get("seconds", "4")
    model = data.get("model", "sora-2")

    try:
        res = asyncio.run(generate_video_prompt(prompt, seconds, model))
        return jsonify({
            "message": "Video prompt processed successfully",
            "video_id": res.id, 
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@ai_video_handler.route("/ai/download-video", methods=["GET"])
def download_video():
    video_id = request.args.get("id")
    if not video_id:
        return jsonify({"error": "No video ID provided"}), 400

    try:
        asyncio.run(download_video_content(video_id))
        return jsonify({
            "message": f"Video {video_id} downloaded successfully"
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ai_video_callback_handler.route("/ai/video/success-callback", methods=["POST"])
def callback_success():
    data = request.get_json()
    video_id = data["data"]["id"]
    print(f"Video {video_id} processing completed.")
    asyncio.run(download_video_content(video_id))
    return jsonify({"message": "Callback received", "data": data}), 200