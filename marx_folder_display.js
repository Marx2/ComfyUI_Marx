import {app} from "../../scripts/app.js";

// Add folder path display to Marx Load Image nodes
app.registerExtension({
  name: "Marx.FolderPathDisplay",
  async beforeRegisterNodeDef(nodeType, nodeData, app) {
    // Check if this is one of our Marx Load Image nodes
    if (nodeData.name && nodeData.name.startsWith("MarxLoadImage")) {
      const onNodeCreated = nodeType.prototype.onNodeCreated;

      nodeType.prototype.onNodeCreated = function () {
        const result = onNodeCreated?.apply(this, arguments);

        // Extract folder number from node name (MarxLoadImage1 -> 1)
        const folderNumber = nodeData.name.replace("MarxLoadImage", "");

        // Get the configured folder path from settings
        const settingKey = `Marx.folder${folderNumber}`;
        let folderPath = app.ui.settings.getSettingValue(settingKey);

        // Default folder paths if not configured
        const defaultFolders = {
          "1": "e",
          "2": "f",
          "3": "g",
          "4": "h",
          "5": "i"
        };

        if (!folderPath || folderPath === "") {
          folderPath = defaultFolders[folderNumber] || "e";
        }

        // Store the folder path on the node
        this.folderPath = folderPath;

        // Add folder path to node title
        const originalTitle = this.title || nodeData.display_name
            || nodeData.name;
        this.title = `${originalTitle}\n📁 input/${folderPath}`;

        return result;
      };

      // Also add visual feedback in node rendering
      const onDrawForeground = nodeType.prototype.onDrawForeground;
      nodeType.prototype.onDrawForeground = function (ctx) {
        const result = onDrawForeground?.apply(this, arguments);

        if (this.folderPath) {
          // Draw folder path below the node title area
          ctx.save();
          ctx.font = "11px monospace";
          ctx.fillStyle = "#999";
          ctx.textAlign = "left";
          const text = `📁 input/${this.folderPath}`;
          ctx.fillText(text, 15, 45);
          ctx.restore();
        }

        return result;
      };
    }
  },
});

