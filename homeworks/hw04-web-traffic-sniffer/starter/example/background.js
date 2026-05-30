chrome.webRequest.onBeforeRequest.addListener(
  async (details) => {
    if (details.requestBody) {

      if (details.requestBody.raw) {
        // decode raw data
        console.group(`📦 [Request] ${details.url}`);
        
        try {
          // parse to json
        } catch (e) {
          console.log("🔸 Original Raw String:", rawString);
        }
        console.groupEnd();
      }
    }
  },
  { urls: ["<all_urls>"] },
  ["requestBody"]
);

console.log(">>> Network Sniffer Loaded");