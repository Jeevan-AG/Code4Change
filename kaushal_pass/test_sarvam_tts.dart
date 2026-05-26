import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:flutter_dotenv/flutter_dotenv.dart';

void main() async {
  final apiKey = 'sk_x9l3uxxx_5N2WhYswqp07fDAcbqxRxYpR'; // From .env
  
  print('Testing TTS...');
  try {
    final response = await http.post(
      Uri.parse('https://api.sarvam.ai/text-to-speech'),
      headers: {
        'api-subscription-key': apiKey,
        'Content-Type': 'application/json',
      },
      body: jsonEncode({
        "text": "Hello, this is a test.",
        "speaker": "shubh",
        "model": "bulbul:v3",
        "target_language_code": "en-IN"
      }),
    );
    print('Status Code: \${response.statusCode}');
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      print('Response Keys: \${data.keys.toList()}');
    } else {
      print('Error Body: \${response.body}');
    }
  } catch (e) {
    print('Error: \$e');
  }
}
