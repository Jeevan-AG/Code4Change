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
        "inputs": ["Hello, this is a test."],
        "target_language_code": "en-IN",
        "speaker": "priya",
        "model": "bulbul:v3"
      }),
    );
    print('With inputs: Status Code: ' + response.statusCode.toString());
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      print('Response Keys: ' + data.keys.toList().toString());
    } else {
      print('Error Body: ' + response.body);
    }
  } catch (e) {
    print('Error: ' + e.toString());
  }
}
