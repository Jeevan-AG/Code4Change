import 'dart:convert';
import 'package:http/http.dart' as http;

void main() async {
  final apiKey = 'sk_x9l3uxxx_5N2WhYswqp07fDAcbqxRxYpR';
  
  try {
    final response = await http.post(
      Uri.parse('https://api.sarvam.ai/text-to-speech'),
      headers: {
        'api-subscription-key': apiKey,
        'Content-Type': 'application/json',
      },
      body: jsonEncode({
        "inputs": ["Hello."],
        "target_language_code": "en-IN",
        "speaker": "priya",
        "model": "bulbul:v3"
      }),
    );
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      final b64 = data['audios'][0];
      final bytes = base64Decode(b64);
      final hex = bytes.take(12).map((b) => b.toRadixString(16).padLeft(2, '0')).join(' ');
      print('First bytes: ' + hex);
      // WAV header starts with RIFF ... WAVE (52 49 46 46 ... 57 41 56 45)
    }
  } catch (e) {
    print('Error: ' + e.toString());
  }
}
