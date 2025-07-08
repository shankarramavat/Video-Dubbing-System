def mlalgo(language):
    from transformers import pipeline, MBartForConditionalGeneration, MBart50TokenizerFast
    from datasets import Dataset, Audio
    import soundfile as sf
    import torch
    from aksharamukha import transliterate
    import final_video as final
    import os

    device = "cuda:0" if torch.cuda.is_available() else "cpu"

    # Debug: Print received language from frontend
    print(f"Received language code: {language}")

    # Mapping short codes and full language names
    language_map = {
        "hin": "hindi",
        "hindi": "hindi",
        "mar": "marathi",
        "marathi": "marathi",
        "guj": "gujarati",
        "gujarati": "gujarati",
        "kan": "kannada",
        "kannada": "kannada",
        "tel": "telugu",
        "telugu": "telugu"
    }

    if language not in language_map:
        print(f"❌ Error: Invalid language selected ({language})")
        return

    full_language = language_map[language]  # Convert to full language name
    print(f"✅ Mapped to: {full_language}")

    # Load speech recognition model
    pipe = pipeline(
        "automatic-speech-recognition",
        model="openai/whisper-tiny.en",
        chunk_length_s=30,
        device=device,
    )

    ds = Dataset.from_dict({"audio": ["extracted\\audio_only.mp3"]}).cast_column("audio", Audio())
    sample = ds[0]["audio"]

    prediction = pipe(sample.copy(), batch_size=8)["text"]
    print(f"📝 ASR Output: {prediction}")

    prediction = pipe(sample.copy(), batch_size=8, return_timestamps=False)
    English_text = str(prediction['text'])

    with open("Output\\eng_sub.txt", "w") as file:
        file.write(English_text)
    print("✅ English Subtitle File Saved Successfully")

    # Load translation model
    model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-one-to-many-mmt")
    tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-one-to-many-mmt", src_lang="en_XX")

    # Language translation mapping
    language_code_map = {
        "hindi": "hi_IN",
        "marathi": "mr_IN",
        "gujarati": "gu_IN",
        "kannada": "kan_IN",
        "telugu": "te_IN"
    }

    if full_language in language_code_map:
        tokens = model.generate(
            **tokenizer(English_text, return_tensors="pt"),
            forced_bos_token_id=tokenizer.lang_code_to_id[language_code_map[full_language]]
        )
        trans_text = tokenizer.batch_decode(tokens, skip_special_tokens=True)[0]
    else:
        print("❌ Error: Language not supported for translation.")
        return

    with open("Output\\trans_sub.txt", "w", encoding="utf-8") as file:
        file.write(trans_text)
    print("✅ Translated Subtitle File Saved Successfully")

    # Load Text-to-Speech (TTS) Model
    model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
                              model='silero_tts',
                              language='indic',
                              speaker='v4_indic')

    # Speaker Mapping (Ensuring All Languages Are Covered)
    speaker_map = {
        "hindi": "hindi_male",
        "marathi": "marathi_female",
        "gujarati": "gujarati_female",
        "kannada": "kannada_female",
        "telugu": "telugu_male"
    }

    # Script Mapping for Transliteration
    source_script_map = {
        "hindi": "Devanagari",
        "marathi": "Devanagari",
        "gujarati": "Gujarati",
        "kannada": "Kannada",
        "telugu": "Telugu"
    }

    # Validate and Process TTS
    if full_language in speaker_map and full_language in source_script_map:
        speaker = speaker_map[full_language]

        if speaker not in [
            "bengali_female", "bengali_male", "gujarati_female", "gujarati_male",
            "hindi_female", "hindi_male", "kannada_female", "kannada_male",
            "malayalam_female", "malayalam_male", "manipuri_female",
            "rajasthani_female", "rajasthani_male", "tamil_female", "tamil_male",
            "telugu_female", "telugu_male", "marathi_female", "marathi_male"
        ]:
            print(f"❌ Error: Invalid speaker `{speaker}`")
            return

        roman_text = transliterate.process(source_script_map[full_language], 'ISO', trans_text)
        audio = model.apply_tts(roman_text, speaker=speaker)
    else:
        print("❌ Error: Language not supported for TTS.")
        return

    output_path = 'Output\\translated_audio.mp3'
    sf.write(output_path, audio.squeeze().numpy(), 48000)

    # Combine Video and Audio
    video_file_path = "extracted\\video_without_audio.mp4"
    audio_file_path = "Output\\translated_audio.mp3"
    output_file_path = os.path.join("Final", "dubbed_video.mp4")

    final.combine_video_with_audio(video_file_path, audio_file_path, output_file_path)
    print(f"✅ Dubbed video saved at: {output_file_path}")
