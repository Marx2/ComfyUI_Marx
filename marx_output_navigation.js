import {app} from "../../scripts/app.js";

// Add navigation buttons for Marx Output nodes
app.registerExtension({
  name: "Marx.OutputNavigation",
  async beforeRegisterNodeDef(nodeType, nodeData, app) {
    // Only apply to Output nodes
    if (nodeData.name && nodeData.name.startsWith("MarxLoadOutput")) {
      const onNodeCreated = nodeType.prototype.onNodeCreated;

      nodeType.prototype.onNodeCreated = function () {
        const result = onNodeCreated?.apply(this, arguments);

        const imageWidget = this.widgets?.find(w => w.name === "image");

        if (imageWidget && imageWidget.options && imageWidget.options.values) {
          // Filter to only image files (exclude .DS_Store, etc.)
          const imageExtensions = ['.png', '.jpg', '.jpeg', '.gif', '.webp',
            '.bmp', '.tiff', '.tif', '.avif'];
          this._imageList = imageWidget.options.values.filter(file => {
            const lowerFile = file.toLowerCase();
            return imageExtensions.some(ext => lowerFile.endsWith(ext));
          });
          this._currentImageWidget = imageWidget;

          console.log("=== Marx Output Navigation Init ===");
          console.log("Total files:", imageWidget.options.values.length);
          console.log("Image files:", this._imageList.length);
          console.log("Image list:", this._imageList);
          console.log("Current widget value:", imageWidget.value);

          // Add Previous button
          const prevButton = this.addWidget("button", "◄ Previous", null,
              () => {
                console.log("\n=== Previous Button Clicked ===");
                if (!this._imageList || this._imageList.length === 0) {
                  console.log("ERROR: No image list!");
                  return;
                }

                console.log("Image list length:", this._imageList.length);
                console.log("Widget value BEFORE:", this._currentImageWidget.value);

                // Strip [output] or [input] suffix from widget value
                let currentValue = this._currentImageWidget.value;
                if (currentValue) {
                  currentValue = currentValue.replace(/\s*\[(output|input)\]\s*$/, '');
                }
                console.log("Cleaned value:", currentValue);

                // Always get fresh index from current widget value
                let currentIndex = this._imageList.indexOf(currentValue);
                console.log("Current index:", currentIndex);

                if (currentIndex === -1) {
                  console.log("WARNING: Value not in list, defaulting to 0");
                  currentIndex = 0;
                }

                let newIndex = currentIndex - 1;
                if (newIndex < 0) {
                  newIndex = this._imageList.length - 1;
                  console.log("Wrapped to end");
                }
                console.log("New index:", newIndex);

                const newValue = this._imageList[newIndex];
                console.log("New value:", newValue);

                this._currentImageWidget.value = newValue;
                console.log("Widget value AFTER:", this._currentImageWidget.value);

                if (this._currentImageWidget.callback) {
                  console.log("Calling callback");
                  this._currentImageWidget.callback(newValue);
                } else {
                  console.log("WARNING: No callback!");
                }

                // Force redraw
                if (this.graph && this.graph.canvas) {
                  this.graph.canvas.setDirty(true, true);
                  console.log("Canvas dirty");
                }
                console.log("=== Previous Complete ===\n");
              });

          // Add Next button
          const nextButton = this.addWidget("button", "Next ►", null, () => {
            console.log("\n=== Next Button Clicked ===");
            if (!this._imageList || this._imageList.length === 0) {
              console.log("ERROR: No image list!");
              return;
            }

            console.log("Image list length:", this._imageList.length);
            console.log("Widget value BEFORE:", this._currentImageWidget.value);

            // Strip [output] or [input] suffix from widget value
            let currentValue = this._currentImageWidget.value;
            if (currentValue) {
              currentValue = currentValue.replace(/\s*\[(output|input)\]\s*$/, '');
            }
            console.log("Cleaned value:", currentValue);

            // Always get fresh index from current widget value
            let currentIndex = this._imageList.indexOf(currentValue);
            console.log("Current index:", currentIndex);

            if (currentIndex === -1) {
              console.log("WARNING: Value not in list, defaulting to 0");
              currentIndex = 0;
            }

            let newIndex = currentIndex + 1;
            if (newIndex >= this._imageList.length) {
              newIndex = 0;
              console.log("Wrapped to start");
            }
            console.log("New index:", newIndex);

            const newValue = this._imageList[newIndex];
            console.log("New value:", newValue);

            this._currentImageWidget.value = newValue;
            console.log("Widget value AFTER:", this._currentImageWidget.value);

            if (this._currentImageWidget.callback) {
              console.log("Calling callback");
              this._currentImageWidget.callback(newValue);
            } else {
              console.log("WARNING: No callback!");
            }

            // Force redraw
            if (this.graph && this.graph.canvas) {
              this.graph.canvas.setDirty(true, true);
              console.log("Canvas dirty");
            }
            console.log("=== Next Complete ===\n");
          });

          // Don't serialize button state in workflow
          prevButton.options = {serialize: false};
          nextButton.options = {serialize: false};
        }

        return result;
      };
    }
  },
});

