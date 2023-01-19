from cog import BasePredictor, Input, Path
import os

class Predictor(BasePredictor):
    def setup(self):
        print("moving models to /src")
        os.system("mv -v /train_log /src")

    def predict(self, 
        #video: Path = Input(description="input video"),
        interpolation_factor: int = Input(
            description="interpolation factor. 4 means generate 4 intermediate frames for each input frame",
            default=4),
        ) -> str:
        print("predict")
        
        #os.system(f"python3 inference_video.py --exp={interpolation_factor} --video={video}")
        #out_path = None
        return "hello"

