import os
import asyncio
import gradio as gr
import edge_tts
from src.utils.preprocess import CropAndExtract
from src.test_audio2coeff import Audio2Coeff
from src.facerender.animate import AnimateFromCoeff
from src.generate_batch import get_data
from src.generate_facerender_batch import get_facerender_data
from src.utils.init_path import init_path

# 設定模型路徑與初始化
def TTS_generate(text, voice='zh-TW-HsiaoChenNeural'):
    """將文字轉為語音檔案"""
    output_audio = "input_audio.mp3"
    communicate = edge_tts.Communicate(text, voice)
    asyncio.run(communicate.save(output_audio))
    return output_audio

def generate_anchor_video(source_image, text, voice):
    # 1. 產生音訊
    audio_path = TTS_generate(text, voice)
    
    # 2. 設定 SadTalker 參數 (簡化版邏輯)
    # 注意：實際運行需載入 SadTalker 的相關類別與模型路徑
    # 這裡建議參考 SadTalker 官方的 inference.py 邏輯
    checkpoint_path = './checkpoints'
    config_path = './src/config'
    
    # 假設調用 SadTalker 的核心生成函數
    # 建議直接調用官方提供的推論入口，以下為邏輯示意：
    print(f"正在處理: {source_image} 與 {audio_path}")
    
    # 生成結果路徑 (SadTalker 預設會存放在 results 目錄)
    output_video_path = "results/output_video.mp4"
    
    # 返回生成的影片路徑給 Gradio
    return output_video_path

# 建立 Gradio 介面
with gr.Blocks() as demo:
    gr.Markdown("# 🤖 AI 數位主播生成器")
    
    with gr.Row():
        with gr.Column():
            input_img = gr.Image(type="filepath", label="上傳人像照片")
            input_text = gr.Textbox(label="主播讀稿文字", lines=5, placeholder="請輸入要播報的內容...")
            voice_opt = gr.Dropdown(
                choices=["zh-TW-HsiaoChenNeural", "zh-TW-YunJheNeural", "zh-CN-XiaoxiaoNeural"], 
                value="zh-TW-HsiaoChenNeural", 
                label="選擇語音 (微軟 Edge-TTS)"
            )
            submit_btn = gr.Button("開始生成主播影片", variant="primary")
        
        with gr.Column():
            output_video = gr.Video(label="生成結果")

    submit_btn.click(
        fn=generate_anchor_video,
        inputs=[input_img, input_text, voice_opt],
        outputs=output_video
    )

demo.launch()
