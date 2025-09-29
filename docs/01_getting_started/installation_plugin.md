# Atlas Matrix Plugin

## 📦 Overview
The **Atlas Matrix plugin** is designed to feel just like Maya’s native constraints, making it simple and intuitive to use.  
This plugin extends Maya’s functionality while remaining user-friendly.

---

## 🚀 Installation

1. **Place the plugin folder**  
   Copy the `atlas-matrix` folder into one of the following default paths depending on your OS:
    > 💡 `~` represent your computer root 
   - **Windows**  
     ```bash
     ~/Documents/maya/scripts/
     ```  
   - **macOS**  
     ```bash
     ~/Library/Preferences/Autodesk/maya/scripts/
     ```  
   - **Linux**  
     ```bash
     ~/maya/scripts/
     ```  

   > 💡 You can place the folder anywhere to use the plugin. If you choose a different location, just adjust the path in later steps accordingly.

2. **Launch Maya**  
   Make sure you’re running a supported version of Maya (see the `README.md` for compatibility).

3. **(Required if you didn’t use the default plugin paths)**   
   Drag and drop the `install_plugin.py` file into the Maya viewport.  
   > This script updates `userSetup.py` so Maya knows where to find your custom plugin path.

4. **Enable the plugin in Maya**  
   - Open the **Plugin Manager** in Maya.  
   - Browse to:  

     ```bash
     #Windows 
     ~/Documents/maya/scripts/atlas-matrix/ui/plugin
     ```  

     ```bash
     # MacOs
     ~/Library/Preferences/Autodesk/maya/scripts/atlas-matrix/ui/plugin
     ```  
 
     ```bash
     # Linux
     ~/maya/scripts/atlas-matrix/ui/plugin
     ```
   - Select and load `atlasMatrixConstraint.py`.
    >    Once loaded, you’ll find the Atlas Matrix constraint available in the **Constrain menu** inside Maya.

---

## 🔧 Troubleshooting

- **Plugin not found in Plugin Manager?**  
  Make sure the plugin path is correctly set by using `install_plugin.py`.

- **Maya version not supported?**  
  Double-check the compatibility list in this README.

- **Errors when loading?**  
  Confirm that all files from the `atlas-matrix` folder are intact and not renamed.

- **Can't solve your error?**  
  Take a look at the troubleshooting section `04_troubleshooting` or feel free to contact us on [The Rigging Atlas](www.theriggingatlas.com/contact).

---

## 📖 License
This tool is distributed as-is for non-commercial use.  
For commercial licensing or contributions, please contact the author directly.