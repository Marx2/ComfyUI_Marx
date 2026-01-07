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

          // Add Previous button
          const prevButton = this.addWidget("button", "◄ Previous", null,
              () => {
                if (!this._imageList || this._imageList.length === 0) {
                  return;
                }

                // Strip [output] or [input] suffix from widget value
                let currentValue = this._currentImageWidget.value;
                if (currentValue) {
                  currentValue = currentValue.replace(/\s*\[(output|input)\]\s*$/, '');
                }

                // Get current index from cleaned value
                let currentIndex = this._imageList.indexOf(currentValue);
                if (currentIndex === -1) {
                  currentIndex = 0;
                }

                let newIndex = currentIndex - 1;
                if (newIndex < 0) {
                  newIndex = this._imageList.length - 1;
                }

                const newValue = this._imageList[newIndex];
                this._currentImageWidget.value = newValue;

                if (this._currentImageWidget.callback) {
                  this._currentImageWidget.callback(newValue);
                }

                if (this.graph && this.graph.canvas) {
                  this.graph.canvas.setDirty(true, true);
                }
              });

          // Add Next button
          const nextButton = this.addWidget("button", "Next ►", null, () => {
            if (!this._imageList || this._imageList.length === 0) {
              return;
            }

            // Strip [output] or [input] suffix from widget value
            let currentValue = this._currentImageWidget.value;
            if (currentValue) {
              currentValue = currentValue.replace(/\s*\[(output|input)\]\s*$/, '');
            }

            // Get current index from cleaned value
            let currentIndex = this._imageList.indexOf(currentValue);
            if (currentIndex === -1) {
              currentIndex = 0;
            }

            let newIndex = currentIndex + 1;
            if (newIndex >= this._imageList.length) {
              newIndex = 0;
            }

            const newValue = this._imageList[newIndex];
            this._currentImageWidget.value = newValue;

            if (this._currentImageWidget.callback) {
              this._currentImageWidget.callback(newValue);
            }

            if (this.graph && this.graph.canvas) {
              this.graph.canvas.setDirty(true, true);
            }
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

