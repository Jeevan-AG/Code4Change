import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:camera/camera.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:flutter_tts/flutter_tts.dart';
import '../../profile/data/user_provider.dart';

class AssessmentScreen extends ConsumerStatefulWidget {
  const AssessmentScreen({super.key});

  @override
  ConsumerState<AssessmentScreen> createState() => _AssessmentScreenState();
}

class _AssessmentScreenState extends ConsumerState<AssessmentScreen> {
  CameraController? _cameraController;
  final FlutterTts _flutterTts = FlutterTts();
  bool _isRecording = false;
  bool _isProcessing = false;
  bool _cameraInitialized = false;
  CameraLensDirection _currentLensDirection = CameraLensDirection.front;
  List<CameraDescription> _cameras = [];

  @override
  void initState() {
    super.initState();
    _initializeCamera();
    _initTts();
  }

  void _initTts() async {
    await _flutterTts.setLanguage("en-IN");
    await _flutterTts.setPitch(1.0);
    await _flutterTts.setSpeechRate(0.5);
    // Simulate AI greeting
    Future.delayed(const Duration(seconds: 1), () {
      _flutterTts.speak("Hello! Please turn on the camera and tell me about your work.");
    });
  }

  Future<void> _initializeCamera() async {
    try {
      _cameras = await availableCameras();
      if (_cameras.isNotEmpty) {
        final camera = _cameras.firstWhere(
          (c) => c.lensDirection == _currentLensDirection,
          orElse: () => _cameras.first,
        );
        _cameraController = CameraController(
          camera,
          ResolutionPreset.medium,
          enableAudio: true,
        );
        await _cameraController!.initialize();
        if (mounted) setState(() => _cameraInitialized = true);
      }
    } catch (e) {
      debugPrint("Camera initialization error: $e");
    }
  }

  void _switchCamera() async {
    if (_cameras.length < 2 || _isRecording) return;
    
    _currentLensDirection = _currentLensDirection == CameraLensDirection.front
        ? CameraLensDirection.back
        : CameraLensDirection.front;
        
    setState(() => _cameraInitialized = false);
    await _cameraController?.dispose();
    await _initializeCamera();
  }

  @override
  void dispose() {
    _cameraController?.dispose();
    _flutterTts.stop();
    super.dispose();
  }

  void _toggleRecording() async {
    if (_cameraController == null || !_cameraController!.value.isInitialized) return;

    if (_isRecording) {
      setState(() => _isRecording = false);
      setState(() => _isProcessing = true);
      
      try {
        await _cameraController!.stopVideoRecording();
        await _flutterTts.speak("Thank you. I am analyzing your video now.");
      } catch (e) {
        debugPrint("Stop recording error: \$e");
      }

      await Future.delayed(const Duration(seconds: 4));
      if (mounted) context.push('/result');
    } else {
      try {
        await _cameraController!.startVideoRecording();
        setState(() => _isRecording = true);
        await _flutterTts.speak("I am listening.");
      } catch (e) {
        debugPrint("Start recording error: \$e");
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final user = ref.watch(userProfileProvider);

    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        title: Text('AI Interview - ${user.language}', style: const TextStyle(color: Colors.black87)),
        backgroundColor: Colors.white.withValues(alpha: 0.8),
        iconTheme: const IconThemeData(color: Colors.black87),
        elevation: 0,
        actions: [
          if (!_isRecording && _cameras.length > 1)
            IconButton(
              icon: const Icon(Icons.flip_camera_ios, color: Colors.black87),
              onPressed: _switchCamera,
            ).animate().fadeIn(),
        ],
      ),
      extendBodyBehindAppBar: true,
      body: Stack(
        children: [
          if (_cameraInitialized && _cameraController != null)
            SizedBox.expand(
              child: CameraPreview(_cameraController!),
            )
          else
            const Center(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  CircularProgressIndicator(color: Color(0xFF7C3AED)),
                  SizedBox(height: 16),
                  Text('Initializing Camera...', style: TextStyle(color: Colors.black87, fontSize: 16)),
                ],
              ),
            ),
            
          SafeArea(
            child: Padding(
              padding: const EdgeInsets.all(24.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                    decoration: BoxDecoration(
                      color: Colors.white.withValues(alpha: 0.9),
                      borderRadius: BorderRadius.circular(16),
                      boxShadow: [
                        BoxShadow(color: Colors.black.withValues(alpha: 0.1), blurRadius: 10, offset: const Offset(0, 5))
                      ]
                    ),
                    child: const Text(
                      'AI Voice Assistant is active. Speak in your native language.',
                      textAlign: TextAlign.center,
                      style: TextStyle(color: Colors.black87, fontSize: 16, fontWeight: FontWeight.w500),
                    ),
                  ).animate().fadeIn().slideY(begin: -0.2),
                  const Spacer(),
                  if (_isProcessing)
                    Center(
                      child: Container(
                        padding: const EdgeInsets.all(24),
                        decoration: BoxDecoration(
                          color: Colors.white.withValues(alpha: 0.95),
                          borderRadius: BorderRadius.circular(24),
                          boxShadow: [
                            BoxShadow(color: Colors.black.withValues(alpha: 0.1), blurRadius: 20, offset: const Offset(0, 10))
                          ]
                        ),
                        child: Column(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            const CircularProgressIndicator(color: Color(0xFF7C3AED)),
                            const SizedBox(height: 16),
                            const Text(
                              'AI is analyzing your video...',
                              style: TextStyle(fontSize: 18, color: Colors.black87, fontWeight: FontWeight.bold),
                            ).animate(onPlay: (c) => c.repeat(reverse: true)).fadeIn(),
                          ],
                        ),
                      ),
                    )
                  else
                    Center(
                      child: GestureDetector(
                        onTap: _toggleRecording,
                        child: AnimatedContainer(
                          duration: const Duration(milliseconds: 300),
                          width: _isRecording ? 80 : 70,
                          height: _isRecording ? 80 : 70,
                          decoration: BoxDecoration(
                            shape: BoxShape.circle,
                            border: Border.all(color: _isRecording ? Colors.redAccent : const Color(0xFF7C3AED), width: 4),
                            color: _isRecording ? Colors.redAccent.withValues(alpha: 0.2) : Colors.white,
                            boxShadow: [
                              BoxShadow(color: Colors.black.withValues(alpha: 0.2), blurRadius: 10, offset: const Offset(0, 5))
                            ]
                          ),
                          child: _isRecording
                              ? const Icon(Icons.stop, color: Colors.redAccent, size: 40)
                              : const Icon(Icons.videocam, color: Color(0xFF7C3AED), size: 32),
                        ),
                      ).animate(target: _isRecording ? 1 : 0)
                          .shimmer(duration: 1.seconds, color: Colors.black12),
                    ),
                  const SizedBox(height: 16),
                  if (_isRecording)
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                      decoration: BoxDecoration(
                        color: Colors.white.withValues(alpha: 0.9),
                        borderRadius: BorderRadius.circular(20),
                      ),
                      child: const Text(
                        'Recording & Listening...',
                        textAlign: TextAlign.center,
                        style: TextStyle(color: Colors.redAccent, fontSize: 16, fontWeight: FontWeight.bold),
                      ).animate(onPlay: (c) => c.repeat(reverse: true)).fadeIn(duration: 500.ms),
                    ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
