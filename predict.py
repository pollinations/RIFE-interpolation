from cog import BasePredictor, Input, Path
import os
import tempfile

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
        
        # Create unique temporary filenames
        _, tmp_video_path = tempfile.mkstemp(suffix=".mp4")
        _, out_path = tempfile.mkstemp(suffix=".mp4")
        out_path_final = f"/tmp/interpolated_{interpolation_factor}x_{os.path.basename(tmp_video_path)}"

        try:
            # use ffmpeg to remove duplicate frames
            if os.system(f"ffmpeg -y -i {str(video)} -vf mpdecimate {tmp_video_path}") != 0:
                raise RuntimeError('Error executing ffmpeg to remove duplicate frames')

            if os.system(f"python3 inference_video.py --exp={interpolation_factor} --video=\"{tmp_video_path}\" --output=\"{out_path}\"") != 0:
                raise RuntimeError('Error executing inference_video.py script')

            # reencode with -c:v libx264 -crf 20 -preset slow -vf format=yuv420p -c:a aac -movflags +faststart
            if os.system(f"ffmpeg -y -i {out_path} -c:v libx264 -crf 20 -preset slow -vf format=yuv420p -c:a aac -movflags +faststart {out_path_final}") != 0:
                raise RuntimeError('Error re-encoding the video')


        except Exception as e:
            print(f"Error during prediction: {e}")
            raise

        finally:
            # Cleanup temporary files
            for path in [tmp_video_path, out_path]:
                try:
                    os.remove(path)
                except Exception as e:
                    print(f"Error cleaning up temporary file {path}: {e}")
                    
        return Path(out_path_final)
