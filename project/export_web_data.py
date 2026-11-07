"""Refresh the embedded website data after re-running the experiment."""
from pathlib import Path
import re,json
root=Path(__file__).resolve().parent
page=root.parent/'index.html'
text=page.read_text(encoding='utf-8')
data=(root/'results/experiment.json').read_text(encoding='utf-8')
json.loads(data)
replacement='<script id="experiment-data" type="application/json">'+data.replace('</','<\\/')+'</script>'
text,count=re.subn(r'<script id="experiment-data" type="application/json">.*?</script>',lambda m:replacement,text,count=1,flags=re.S)
assert count==1,'Data container not found'
page.write_text(text,encoding='utf-8')
print('Website data updated')
