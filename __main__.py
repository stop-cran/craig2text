import subprocess
import pysrt
import os
import zipfile

input_zip_path = os.environ['INPUT_ZIP_PATH']

with zipfile.ZipFile(input_zip_path) as input_zip:
    with zipfile.ZipFile(os.path.splitext(input_zip_path)[0] + '-output.zip', 'w',
                        zipfile.ZIP_DEFLATED) as output_zip:
        input_dir = '/tmp/input'
        output_dir = '/tmp/output'

        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)
            output_zip.writestr('info.txt', input_zip.read('info.txt'))

            for audio_file in input_zip.namelist():
                if os.path.splitext(audio_file)[1] == '.aac':
                    input_zip.extract(audio_file, input_dir)

            proc = subprocess.run(['vosk-transcriber', '-l', 'ru',
                                    '-i', input_dir,
                                    '-n', os.environ.get('VOSK_MODEL',
                                                         'vosk-model-ru-0.42'),
                                    '-t', 'srt', '-o', output_dir])

            assert proc.returncode == 0, 'Error processing voice'

        for file in os.listdir(output_dir):
            if os.path.splitext(file)[1] == '.srt':
                file_path = os.path.join(output_dir, file)
                subs = pysrt.open(file_path)
                output_zip.writestr(file[:-4] + '.txt', subs.text)
                with open(file_path, 'r') as srt:
                    output_zip.writestr(file, srt.read())
