"""Captura Firefox aislado, compatible con Pillow opcional y sin servidor web."""
from pathlib import Path
import os
import subprocess
import tempfile
import time

BASE = Path(__file__).resolve().parent.parent

def capture(code, output, width=1440, height=1000):
    html = (BASE / 'index.html').read_text()
    # Evita depender de la red para la tipografía en las capturas locales.
    html = '\n'.join(line for line in html.splitlines() if 'fonts.googleapis.com' not in line and 'fonts.gstatic.com' not in line)
    injection = "<script>document.addEventListener('DOMContentLoaded', () => {" + code + "});</script>"
    harness = BASE / 'harness_temp.html'
    harness.write_text(html.replace('</body>', injection + '</body>'))
    output = Path(output).resolve()
    output.unlink(missing_ok=True)
    with tempfile.TemporaryDirectory(prefix='lingua-firefox-') as profile:
        Path(profile, 'user.js').write_text('user_pref("browser.dom.window.dump.enabled", true);\nuser_pref("datareporting.policy.dataSubmissionEnabled", false);')
        env = dict(os.environ, MOZ_CRASHREPORTER_DISABLE='1', MOZ_DISABLE_CONTENT_SANDBOX='1', MOZ_DISABLE_GMP_SANDBOX='1')
        with tempfile.TemporaryFile(mode='w+') as log:
            proc = subprocess.Popen(['firefox', '--headless', '--no-remote', '--profile', profile, f'--screenshot={output}', f'--window-size={width},{height}', harness.as_uri()], env=env, stdout=log, stderr=log)
            try:
                deadline = time.monotonic() + 25
                while time.monotonic() < deadline:
                    if output.exists() and output.stat().st_size > 1000:
                        time.sleep(.3)
                        break
                    if proc.poll() is not None: break
                    time.sleep(.1)
            finally:
                proc.terminate()
                try: proc.wait(timeout=3)
                except subprocess.TimeoutExpired: proc.kill();proc.wait()
                harness.unlink(missing_ok=True)
            log.seek(0)
            result = log.read()
            if not output.exists(): raise RuntimeError('Firefox no generó captura: ' + result[-1500:])
            return result
