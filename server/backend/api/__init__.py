from flask import Blueprint, jsonify

from ..service import device, media


def create_api(start_time: float) -> Blueprint:
    api = Blueprint("api", __name__, url_prefix="/api")

    @api.errorhandler(media.MediaUnavailable)
    def unavailable(error):
        return jsonify({"error": str(error)}), 501

    @api.route("/status", methods=["GET", "POST"])
    def status():
        return jsonify(device.get_status(start_time))

    @api.get("/media")
    def media_info():
        return media.controller().get_media_info(), 200

    @api.post("/media/next")
    def next_track():
        media.controller().next_track()
        return jsonify({"message": "Success to play next track"})

    @api.post("/media/previous")
    def previous_track():
        media.controller().previous_track()
        return jsonify({"message": "Success to play previous track"})

    @api.post("/media/toggle")
    def toggle():
        media.controller().toggle_play()
        return jsonify({"message": "Success to toggle play/pause"})

    return api
