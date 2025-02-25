import os, speedtest

# This Appwrite function will be executed every time your function is triggered
def main(context):
    # You can use the Appwrite SDK to interact with other services
    # For this example, we're using the Users service
    if context.req.query and 'results' in context.req.query:
        context.log(f"measuring..")
        st = speedtest.Speedtest(secure=True)
        st.get_best_server()
        download_speed = st.download() / 1e6  # Convert from bits/s to Mbps
        upload_speed = st.upload() / 1e6  # Convert from bits/s to Mbps
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

    with open("speedtest.html", "r", encoding="utf-8") as file:
        html_text = file.read()
        return context.res.text(html_text, 200, {"content-type": "text/html"})
