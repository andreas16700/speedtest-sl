import os

def trigger_update(context):
    import speedtest
    from appwrite.id import ID
    from appwrite.services.databases import Databases
    from appwrite.client import Client

    client = (
        Client()
        .set_endpoint(os.environ["APPWRITE_FUNCTION_API_ENDPOINT"])
        .set_project(os.environ["APPWRITE_FUNCTION_PROJECT_ID"])
        .set_key(context.req.headers["x-appwrite-key"])
    )

    databases = Databases(client)

    dbid = "meta"
    collid = "speedtest"

    def create_doc(ts, host, server, latency, ul=None, dl=None):
        d = {
            'timestamp': ts,
            'host': host,
            'server': server,
            'latency': latency,
        }
        if dl and dl != 0:
            d['download'] = dl
        if ul and ul != 0:
            d['upload'] = ul
        doc = databases.create_document(database_id=dbid, collection_id=collid, document_id=id, data=d)
        return doc

    def update_doc(doc_id, ul=None, dl=None):
        d = {}
        if dl and dl != 0:
            d['download'] = dl
        if ul and ul != 0:
            d['upload'] = ul
        doc = databases.update_document(database_id=dbid, collection_id=collid, document_id=doc_id, data=d)
        return doc

    id = ID.unique()

    st = speedtest.Speedtest(secure=True)

    st.get_best_server()
    r = st.results
    server = f"{r.server['sponsor']} - {r.server['name']}"
    create_doc(ts=r.timestamp, host=r.server['host'], server=server, latency=r.server['latency'])
    download_speed = st.download() / 1e6  # Convert from bits/s to Mbps
    print(f"measured download speed: {download_speed}")
    update_doc(doc_id=id, dl=download_speed)

    upload_speed = st.upload() / 1e6  # Convert from bits/s to Mbps
    print(f"measured upload speed: {upload_speed}")
    update_doc(doc_id=id, ul=upload_speed)
    return download_speed, upload_speed


# This Appwrite function will be executed every time your function is triggered
def main(context):

    if context.req.query and 'results' in context.req.query:
        context.log(f"measuring..")
        download_speed, upload_speed = trigger_update(context)
        context.log(f"measured download speed: {download_speed} upload speed: {upload_speed}")
        return context.res.text(f"""<div id="speed-test-results">
      <div class="speed">
        <div>
          <h2>{download_speed:.2f} Mbps</h2>
          <p>Download Speed</p>
        </div>
        <div>
          <h2>{upload_speed:.2f} Mbps</h2>
          <p>Upload Speed</p>
        </div>
      </div>
    </div>
    """, 200, {"content-type": "text/html"})

    # Get the directory where the current script is located
    script_dir = os.path.dirname(__file__)

    # Build the full path to the file
    file_path = os.path.join(script_dir, 'speedtest.html')
    with open(file_path, "r", encoding="utf-8") as file:
        html_text = file.read()
        return context.res.text(html_text, 200, {"content-type": "text/html"})
