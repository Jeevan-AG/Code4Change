import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'dart:ui';
import '../../profile/data/user_provider.dart';

class OnboardingScreen extends ConsumerStatefulWidget {
  const OnboardingScreen({super.key});

  @override
  ConsumerState<OnboardingScreen> createState() => _OnboardingScreenState();
}

class _OnboardingScreenState extends ConsumerState<OnboardingScreen> {
  bool _isListening = false;
  bool _isProcessing = false;
  
  final _nameController = TextEditingController();
  final _stateController = TextEditingController();
  final _occupationController = TextEditingController();
  String _selectedLanguage = 'English';

  @override
  void dispose() {
    _nameController.dispose();
    _stateController.dispose();
    _occupationController.dispose();
    super.dispose();
  }

  void _toggleListening() async {
    if (_isListening) {
      // Stop listening and start processing
      setState(() {
        _isListening = false;
        _isProcessing = true;
      });

      // Simulate AI extraction
      await Future.delayed(const Duration(seconds: 2));

      if (!mounted) return;

      setState(() {
        _nameController.text = 'Priya Sharma';
        _stateController.text = 'Maharashtra';
        _occupationController.text = 'Bridal Mehendi Artist';
        _selectedLanguage = 'Hindi';
        _isProcessing = false;
      });
    } else {
      // Start listening indefinitely until tapped again
      setState(() {
        _isListening = true;
        _isProcessing = false;
      });
    }
  }

  void _completeOnboarding() async {
    final profile = UserProfile(
      name: _nameController.text.isNotEmpty ? _nameController.text : 'User',
      state: _stateController.text,
      language: _selectedLanguage,
      occupation: _occupationController.text,
    );
    await ref.read(userProfileProvider.notifier).updateProfile(profile);
    if (mounted) {
      context.go('/dashboard');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: Container(
        height: MediaQuery.of(context).size.height,
        width: double.infinity,
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [Color(0xFFFFEAD2), Color(0xFFE6EFFF)],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
        ),
        child: SafeArea(
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(24.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                const Text(
                  'Tell us about yourself',
                  style: TextStyle(fontSize: 32, fontWeight: FontWeight.bold, color: Colors.black87),
                  textAlign: TextAlign.center,
                ).animate().fadeIn(duration: 600.ms).slideY(begin: -0.2),
                
                const SizedBox(height: 8),
                const Text(
                  'Fill the form below, or just tap the mic and tell us!',
                  style: TextStyle(fontSize: 16, color: Colors.black54),
                  textAlign: TextAlign.center,
                ).animate().fadeIn(delay: 200.ms),
                
                const SizedBox(height: 32),

                // Voice Recording Area
                if (_isProcessing)
                  const Column(
                    children: [
                      CircularProgressIndicator(color: Color(0xFF7C3AED)),
                      SizedBox(height: 16),
                      Text('AI is filling out the form...', style: TextStyle(color: Colors.black87, fontSize: 16)),
                    ],
                  ).animate().fadeIn()
                else
                  Center(
                    child: GestureDetector(
                      onTap: _toggleListening,
                      child: AnimatedContainer(
                        duration: const Duration(milliseconds: 300),
                        width: _isListening ? 100 : 80,
                        height: _isListening ? 100 : 80,
                        decoration: BoxDecoration(
                          shape: BoxShape.circle,
                          color: _isListening ? Colors.redAccent : const Color(0xFF7C3AED).withValues(alpha: 0.1),
                          border: Border.all(color: _isListening ? Colors.redAccent : const Color(0xFF7C3AED), width: _isListening ? 4 : 2),
                          boxShadow: _isListening ? [
                            BoxShadow(color: Colors.redAccent.withValues(alpha: 0.5), blurRadius: 20, spreadRadius: 5)
                          ] : [],
                        ),
                        child: Icon(
                          _isListening ? Icons.mic : Icons.mic_none,
                          size: 40,
                          color: _isListening ? Colors.white : const Color(0xFF7C3AED),
                        ),
                      ),
                    ).animate(target: _isListening ? 1 : 0)
                        .shimmer(duration: 1.seconds, color: Colors.black12),
                  ).animate().fadeIn(delay: 300.ms).scale(),

                if (_isListening) ...[
                  const SizedBox(height: 16),
                  const Text(
                    'Listening...',
                    textAlign: TextAlign.center,
                    style: TextStyle(color: Colors.redAccent, fontSize: 16, fontWeight: FontWeight.bold),
                  ).animate(onPlay: (c) => c.repeat(reverse: true)).fadeIn(duration: 500.ms),
                ],

                const SizedBox(height: 40),

                // Form Area
                Container(
                  padding: const EdgeInsets.all(24),
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(20),
                    boxShadow: [
                      BoxShadow(color: Colors.black.withValues(alpha: 0.05), blurRadius: 20, offset: const Offset(0, 10))
                    ]
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      _buildTextField('Full Name', _nameController, Icons.person),
                      const SizedBox(height: 20),
                      _buildTextField('State', _stateController, Icons.location_on),
                      const SizedBox(height: 20),
                      _buildDropdown(),
                      const SizedBox(height: 20),
                      _buildTextField('Occupation', _occupationController, Icons.work),
                    ],
                  ),
                ).animate().fadeIn(delay: 400.ms).slideY(begin: 0.2),

                const SizedBox(height: 40),

                // Submit Button
                FilledButton(
                  onPressed: _completeOnboarding,
                  style: FilledButton.styleFrom(
                    backgroundColor: const Color(0xFF7C3AED),
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                  ),
                  child: const Text('Complete Setup', style: TextStyle(fontSize: 18, color: Colors.white, fontWeight: FontWeight.bold)),
                ).animate().fadeIn(delay: 600.ms),
                const SizedBox(height: 24),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildTextField(String label, TextEditingController controller, IconData icon) {
    return TextFormField(
      controller: controller,
      style: const TextStyle(color: Colors.black87),
      decoration: InputDecoration(
        labelText: label,
        labelStyle: const TextStyle(color: Colors.black54),
        prefixIcon: Icon(icon, color: Colors.black54),
        filled: true,
        fillColor: Colors.black.withValues(alpha: 0.03),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(16),
          borderSide: BorderSide.none,
        ),
      ),
    );
  }

  Widget _buildDropdown() {
    return DropdownButtonFormField<String>(
      decoration: InputDecoration(
        labelText: 'Preferred Language',
        labelStyle: const TextStyle(color: Colors.black54),
        prefixIcon: const Icon(Icons.language, color: Colors.black54),
        filled: true,
        fillColor: Colors.black.withValues(alpha: 0.03),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(16),
          borderSide: BorderSide.none,
        ),
      ),
      dropdownColor: Colors.white,
      style: const TextStyle(color: Colors.black87, fontSize: 16),
      initialValue: _selectedLanguage,
      items: ['English', 'Hindi', 'Tamil', 'Telugu', 'Kannada', 'Bengali'].map((lang) {
        return DropdownMenuItem(value: lang, child: Text(lang));
      }).toList(),
      onChanged: (val) {
        if (val != null) setState(() => _selectedLanguage = val);
      },
    );
  }
}
