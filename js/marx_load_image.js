import {app} from "../../scripts/app.js";
import {api} from "../../scripts/api.js";

app.registerExtension({
  name: "Marx.LoadImage",
  async beforeRegisterNodeDef(nodeType, nodeData, app) {
    if (nodeData.name === "MarxLoadImage") {
      const onNodeCreated = nodeType.prototype.onNodeCreated;
      nodeType.prototype.onNodeCreated = function () {
        const ret = onNodeCreated ? onNodeCreated.apply(this, arguments)
            : undefined;

        const folderWidget = this.widgets.find(w => w.name === "folder");
        const imageWidget = this.widgets.find(w => w.name === "image");

        if (folderWidget && imageWidget) {
          // Store original callback
          const originalCallback = folderWidget.callback;

          // Override folder widget callback
          folderWidget.callback = async function () {
            if (originalCallback) {
              originalCallback.apply(this, arguments);
            }

            // Get images for selected folder
            const folder = folderWidget.value;
            try {
              const resp = await api.fetchApi("/marx/images", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({folder: folder})
              });

              if (resp.ok) {
                const data = await resp.json();
                const images = data.images || [];

                // Update image widget options
                imageWidget.options.values = images;

                // Set first image as default if available
                if (images.length > 0) {
                  imageWidget.value = images[0];
                } else {
                  imageWidget.value = "";
                }
              }
            } catch (error) {
              console.error("Error fetching images:", error);
            }
          };

          // Trigger initial load
          if (folderWidget.value) {
            folderWidget.callback();
          }
        }

        return ret;
      };
    }
  }
});

