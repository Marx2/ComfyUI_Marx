import {app} from "../../scripts/app.js";

// Add folder path display to Marx Load Image nodes
app.registerExtension({
  name: "Marx.FolderPathDisplay",
  async beforeRegisterNodeDef(nodeType, nodeData, app) {
    // Check if this is one of our Marx Load Image nodes
    if (nodeData.name && (nodeData.name.startsWith("MarxLoadInput")
        || nodeData.name.startsWith("MarxLoadOutput"))) {
      const onNodeCreated = nodeType.prototype.onNodeCreated;

      nodeType.prototype.onNodeCreated = function () {
        const result = onNodeCreated?.apply(this, arguments);

        // Extract folder type and number from node name
        // MarxLoadInputImage1 -> type: Input, number: 1
        // MarxLoadOutputImage2 -> type: Output, number: 2
        let folderType = "";
        let folderNumber = "";

        if (nodeData.name.includes("Input")) {
          folderType = "Input";
          folderNumber = nodeData.name.replace("MarxLoadInputImage", "");
        } else if (nodeData.name.includes("Output")) {
          folderType = "Output";
          folderNumber = nodeData.name.replace("MarxLoadOutputImage", "");
        }

        // Get the configured folder path from settings
        const settingKey = `Marx.folder${folderType}${folderNumber}`;
        let folderPath = app.ui.settings.getSettingValue(settingKey);

        // Default folder paths if not configured
        const defaultFolders = {
          "Input1": "input1",
          "Input2": "input2",
          "Input3": "input3",
          "Output1": "output1",
          "Output2": "output2",
          "Output3": "output3"
        };

        if (!folderPath || folderPath === "") {
          folderPath = defaultFolders[`${folderType}${folderNumber}`]
              || "input1";
        }

        // Store the folder path on the node
        this.folderPath = folderPath;
        this.folderType = folderType.toLowerCase(); // "input" or "output"

        // Add folder path to node title with appropriate base directory
        const originalTitle = this.title || nodeData.display_name
            || nodeData.name;
        const basePath = folderType.toLowerCase() === "input" ? "input"
            : "output";
        this.title = `${originalTitle}\n📁 ${basePath}/${folderPath}`;

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
          const basePath = this.folderType === "input" ? "input" : "output";
          const text = `📁 ${basePath}/${this.folderPath}`;
          ctx.fillText(text, 15, 45);
          ctx.restore();
        }

        return result;
      };
    }
  },
});

