# WindowsObfuscation

This is a python based automation tool I created that obfuscates a powershell reverse TCP payload generated using Villain framework and prepares it for embedding into a microsoft word VBA macro. After the document is opened it creates a backdoor in a targeted system bypassing windows defender.

The primary purpose of the code is to:
1. Randomize powershell variable names
2. Randomize function names
3. Convert the payload into a single-line format
4. Generate a ready to use VBA macro (macro.vba) that executes the obfuscated powershell command invisibly on document open

Workflow:
1. Generate a reverse TCP payload using the Villain framework or use the one i uploaded.
2. Insert the payload into the Python script.
3. Run the obfuscator.
4. Copy the generated VBA macro into a word document.
5. Save the document as a macro enabled file (.docm).
