import {app} from "../../scripts/app.js";

// Register settings for Marx custom node
app.registerExtension({
  name: "Marx.Settings",
  async setup() {
    // Register custom settings in ComfyUI's settings panel
    app.ui.settings.addSetting({
      id: "Marx.folderInput1",
      name: "Marx Folder Input 1",
      type: "text",
      defaultValue: "input1",
      tooltip: "Subfolder path in ComfyUI/input directory for Load Input Image 1",
      attrs: {
        style: {
          fontFamily: "monospace",
        }
      }
    });

    app.ui.settings.addSetting({
      id: "Marx.folderInput2",
      name: "Marx Folder Input 2",
      type: "text",
      defaultValue: "input2",
      tooltip: "Subfolder path in ComfyUI/input directory for Load Input Image 2",
      attrs: {
        style: {
          fontFamily: "monospace",
        }
      }
    });

    app.ui.settings.addSetting({
      id: "Marx.folderInput3",
      name: "Marx Folder Input 3",
      type: "text",
      defaultValue: "input3",
      tooltip: "Subfolder path in ComfyUI/input directory for Load Input Image 3",
      attrs: {
        style: {
          fontFamily: "monospace",
        }
      }
    });

    app.ui.settings.addSetting({
      id: "Marx.folderOutput1",
      name: "Marx Folder Output 1",
      type: "text",
      defaultValue: "output1",
      tooltip: "Subfolder path in ComfyUI/input directory for Load Output Image 1",
      attrs: {
        style: {
          fontFamily: "monospace",
        }
      }
    });

    app.ui.settings.addSetting({
      id: "Marx.folderOutput2",
      name: "Marx Folder Output 2",
      type: "text",
      defaultValue: "output2",
      tooltip: "Subfolder path in ComfyUI/input directory for Load Output Image 2",
      attrs: {
        style: {
          fontFamily: "monospace",
        }
      }
    });

    app.ui.settings.addSetting({
      id: "Marx.folderOutput3",
      name: "Marx Folder Output 3",
      type: "text",
      defaultValue: "output3",
      tooltip: "Subfolder path in ComfyUI/input directory for Load Output Image 3",
      attrs: {
        style: {
          fontFamily: "monospace",
        }
      }
    });
  },
});

