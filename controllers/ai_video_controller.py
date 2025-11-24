from flask_restx import Namespace, Resource, fields, reqparse
import asyncio
from services.ai_video.video import generate_video_prompt, download_video_content

# Namespace untuk AI Video
ai_video_ns = Namespace("AI Video", description="Endpoints untuk AI video generation")
ai_video_callback_ns = Namespace("AI Video Callback", description="Callback dari AI Video Service")

# Model untuk POST /ai/video-prompt
video_prompt_model = ai_video_ns.model("VideoPrompt", {
    "prompt": fields.String(required=True, description="Text prompt untuk video"),
    "seconds": fields.String(required=False, description="Durasi video dalam detik", default="4"),
    "model": fields.String(required=False, description="Model AI yang digunakan", default="sora-2")
})

# Model response
video_response_model = ai_video_ns.model("VideoResponse", {
    "message": fields.String,
    "video_id": fields.String
})

# Parser untuk query param GET /ai/download-video
download_parser = reqparse.RequestParser()
download_parser.add_argument("id", required=True, help="Video ID harus diberikan", location="args")


# ------------------- ROUTES -------------------

@ai_video_ns.route("/video-prompt")
class VideoPrompt(Resource):
    @ai_video_ns.expect(video_prompt_model)
    @ai_video_ns.marshal_with(video_response_model)
    def post(self):
        """Proses video dari prompt AI"""
        data = ai_video_ns.payload
        prompt = data["prompt"]
        seconds = data.get("seconds", "4")
        model = data.get("model", "sora-2")

        try:
            res = asyncio.run(generate_video_prompt(prompt, seconds, model))
            return {
                "message": "Video prompt processed successfully",
                "video_id": res.id
            }, 200
        except Exception as e:
            ai_video_ns.abort(500, str(e))


@ai_video_ns.route("/download-video")
class DownloadVideo(Resource):
    @ai_video_ns.expect(download_parser)
    def get(self):
        """Download video berdasarkan video_id"""
        args = download_parser.parse_args()
        video_id = args["id"]

        try:
            asyncio.run(download_video_content(video_id))
            return {
                "message": f"Video {video_id} downloaded successfully"
            }, 200
        except Exception as e:
            ai_video_ns.abort(500, str(e))


# ------------------- CALLBACK -------------------

callback_model = ai_video_callback_ns.model("VideoCallback", {
    "data": fields.Raw(required=True, description="Data callback dari AI service")
})

@ai_video_callback_ns.route("/video/success-callback")
class CallbackSuccess(Resource):
    @ai_video_callback_ns.expect(callback_model)
    def post(self):
        """Callback ketika video berhasil diproses"""
        data = ai_video_callback_ns.payload
        video_id = data["data"]["id"]
        print(f"Video {video_id} processing completed.")
        asyncio.run(download_video_content(video_id))
        return {"message": "Callback received", "data": data}, 200
