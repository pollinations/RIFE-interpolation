from cog import BasePredictor, Input, Path
import os

class Predictor(BasePredictor):
    def setup(self):
        print("moving models to /src")
        os.system("cp -rv /train_log/* /src/train_log")

    def predict(self, 
        video: Path = Input(description="input video"),
        interpolation_factor: int = Input(
            description="interpolation factor. 4 means generate 4 intermediate frames for each input frame",
            default=4),
        ) -> Path:
        print("predict")
        # os.system("rm /tmp/*.mp4")
        
        out_path = f"/tmp/interpolated.mp4"
        out_path_final = f"/tmp/interpolated_{interpolation_factor}x.mp4"

        # use ffmpeg to remove duplicate frames
        os.system(f"ffmpeg -i {str(video)} -vf mpdecimate {str(video)}_nodup.mp4")


        # os.system(f"rm -rf {out_path}")
        os.system(f"python3 inference_video.py --exp={interpolation_factor} --video=\"{str(video)}\" --output=\"{out_path}\"") 

        # reencode with -c:v libx264 -crf 20 -preset slow -vf format=yuv420p -c:a aac -movflags +faststart

        os.system(f"ffmpeg -i {out_path} -c:v libx264 -crf 20 -preset slow -vf format=yuv420p -c:a aac -movflags +faststart {out_path_final}")

        os.system("ls -l /src")
        os.system("ls -l /tmp")

        return Path(out_path_final)

