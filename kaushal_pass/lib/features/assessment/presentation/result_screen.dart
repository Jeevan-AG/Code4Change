import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:flutter_animate/flutter_animate.dart';

class ResultScreen extends StatelessWidget {
  const ResultScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      extendBodyBehindAppBar: true,
      appBar: AppBar(
        title: const Text('AI Analysis Result', style: TextStyle(color: Colors.black87)),
        backgroundColor: Colors.transparent,
        elevation: 0,
        iconTheme: const IconThemeData(color: Colors.black87),
      ),
      body: Container(
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
                const SizedBox(height: 20),
                const Icon(Icons.verified, size: 80, color: Colors.green)
                    .animate()
                    .scale(duration: 600.ms, curve: Curves.easeOutBack)
                    .shimmer(duration: 1.seconds),
                const SizedBox(height: 16),
                const Text(
                  'Bridal Mehendi Artist',
                  textAlign: TextAlign.center,
                  style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: Colors.black87),
                ).animate().fadeIn(delay: 200.ms).slideY(),
                const SizedBox(height: 12),
                Center(
                  child: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                    decoration: BoxDecoration(
                      color: const Color(0xFF7C3AED).withValues(alpha: 0.1),
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: const Text(
                      'NSQF Level 4',
                      style: TextStyle(color: Color(0xFF7C3AED), fontWeight: FontWeight.bold, fontSize: 16),
                    ),
                  ).animate().fadeIn(delay: 400.ms).scale(),
                ),
                const SizedBox(height: 32),
                
                // What She Can Do
                _buildSectionHeader('Verified Skills (What you can do)', Icons.check_circle_outline),
                _buildGlassCard(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      _buildBulletPoint('Expert in Arabic and traditional bridal designs.'),
                      _buildBulletPoint('Understands color mixing and long-lasting mehendi techniques.'),
                      _buildBulletPoint('Can comfortably manage 5-10 clients per event.'),
                      _buildBulletPoint('Good communication and client management skills.'),
                    ],
                  ),
                ).animate().fadeIn(delay: 600.ms).slideX(begin: -0.2),
                
                const SizedBox(height: 24),
                
                // Trust Rating & Factors
                _buildSectionHeader('Trust Rating: 8.5/10', Icons.shield_outlined),
                _buildGlassCard(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text('Why this score?', style: TextStyle(color: Colors.black87, fontWeight: FontWeight.bold, fontSize: 16)),
                      const SizedBox(height: 8),
                      _buildFactorPoint('High Video Clarity: Face and work were clearly visible.', Colors.green),
                      _buildFactorPoint('Confident Speech: Audio matched visual demonstration perfectly.', Colors.green),
                      _buildFactorPoint('Missing Peer Verification: Could improve score to 10/10 if a community member verifies.', Colors.amber.shade700),
                    ],
                  ),
                ).animate().fadeIn(delay: 800.ms).slideX(begin: 0.2),

                const SizedBox(height: 24),

                // Entrepreneurship Roadmap
                _buildSectionHeader('Entrepreneurship Roadmap', Icons.moving),
                _buildGlassCard(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text('Next Steps to grow your business:', style: TextStyle(color: Colors.black54, fontSize: 14)),
                      const SizedBox(height: 16),
                      _buildRoadmapStep(1, 'Apply for PM Mudra Loan', 'Eligible for up to ₹50,000 to buy bulk mehendi supplies.'),
                      _buildRoadmapStep(2, 'Join CredOra Marketplace', 'List your services online to get booked for weddings.'),
                      _buildRoadmapStep(3, 'Hire 2 Assistants', 'Your skill level allows you to train and manage junior artists.'),
                    ],
                  ),
                ).animate().fadeIn(delay: 1000.ms).slideY(begin: 0.2),

                const SizedBox(height: 40),
                SizedBox(
                  width: double.infinity,
                  child: FilledButton.icon(
                    onPressed: () => context.push('/passport'),
                    icon: const Icon(Icons.wallet, color: Colors.white),
                    label: const Text('Add to Passport'),
                    style: FilledButton.styleFrom(
                      backgroundColor: const Color(0xFF7C3AED),
                      foregroundColor: Colors.white,
                      padding: const EdgeInsets.symmetric(vertical: 20),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(20),
                      ),
                      textStyle: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                    ),
                  ),
                ).animate().fadeIn(delay: 1200.ms).slideY(begin: 0.2, end: 0),
                const SizedBox(height: 24),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildSectionHeader(String title, IconData icon) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Row(
        children: [
          Icon(icon, color: const Color(0xFF7C3AED), size: 20),
          const SizedBox(width: 8),
          Text(title, style: const TextStyle(color: Colors.black87, fontSize: 18, fontWeight: FontWeight.bold)),
        ],
      ),
    );
  }

  Widget _buildGlassCard({required Widget child}) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(color: Colors.black.withValues(alpha: 0.05), blurRadius: 20, offset: const Offset(0, 10))
        ]
      ),
      child: child,
    );
  }

  Widget _buildBulletPoint(String text) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('• ', style: TextStyle(color: Color(0xFF7C3AED), fontSize: 16, fontWeight: FontWeight.bold)),
          Expanded(child: Text(text, style: const TextStyle(color: Colors.black87, fontSize: 14))),
        ],
      ),
    );
  }

  Widget _buildFactorPoint(String text, Color iconColor) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(Icons.stop_circle, color: iconColor, size: 16),
          const SizedBox(width: 8),
          Expanded(child: Text(text, style: const TextStyle(color: Colors.black54, fontSize: 14))),
        ],
      ),
    );
  }

  Widget _buildRoadmapStep(int step, String title, String description) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: Colors.blue.withValues(alpha: 0.1),
              shape: BoxShape.circle,
            ),
            child: Text(step.toString(), style: const TextStyle(color: Colors.blue, fontWeight: FontWeight.bold)),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title, style: const TextStyle(color: Colors.black87, fontWeight: FontWeight.bold, fontSize: 16)),
                const SizedBox(height: 4),
                Text(description, style: const TextStyle(color: Colors.black54, fontSize: 14)),
              ],
            ),
          )
        ],
      ),
    );
  }
}
