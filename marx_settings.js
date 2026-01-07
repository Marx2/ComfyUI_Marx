import {app} from "../../scripts/app.js";

// Register settings for Marx custom node
app.registerExtension({
  name: "Marx.Settings",
  async setup() {
    // Register custom settings in ComfyUI's settings panel
    app.ui.settings.addSetting({
      id: "Marx.folder1",
      name: "Marx Folder 1",
      type: "text",
      defaultValue: "e",
      tooltip: "Subfolder path in ComfyUI/input directory for image selector 1",
      attrs: {
        style: {
          fontFamily: "monospace",
        }
      }
    });

    app.ui.settings.addSetting({
      id: "Marx.folder2",
      name: "Marx Folder 2",
      type: "text",
      defaultValue: "f",
      tooltip: "Subfolder path in ComfyUI/input directory for image selector 2",
      attrs: {
        style: {
          fontFamily: "monospace",
        }
      }
    });

    app.ui.settings.addSetting({
      id: "Marx.folder3",
      name: "Marx Folder 3",
      type: "text",
      defaultValue: "g",
      tooltip: "Subfolder path in ComfyUI/input directory for image selector 3",
      attrs: {
        style: {
          fontFamily: "monospace",
        }
      }
    });

    app.ui.settings.addSetting({
      id: "Marx.folder4",
      name: "Marx Folder 4",
      type: "text",
      defaultValue: "h",
      tooltip: "Subfolder path in ComfyUI/input directory for image selector 4",
      attrs: {
        style: {
          fontFamily: "monospace",
        }
      }
    });

    app.ui.settings.addSetting({
      id: "Marx.folder5",
      name: "Marx Folder 5",
      type: "text",
      defaultValue: "i",
      tooltip: "Subfolder path in ComfyUI/input directory for image selector 5",
      attrs: {
        style: {
          fontFamily: "monospace",
        }
      }
    });
  },
});

