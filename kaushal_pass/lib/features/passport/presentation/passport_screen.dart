import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:qr_flutter/qr_flutter.dart';
import 'package:pdf/pdf.dart';
import 'package:pdf/widgets.dart' as pw;
import 'package:printing/printing.dart';
import 'package:flutter_animate/flutter_animate.dart';
import '../../profile/data/user_provider.dart';

class PassportScreen extends ConsumerWidget {
  const PassportScreen({super.key});

  Future<void> _generateAndPrintPDF(UserProfile user) async {
    final pdf = pw.Document();
    
    pdf.addPage(
      pw.Page(
        pageFormat: PdfPageFormat.a4,
        build: (pw.Context context) {
          return pw.Center(
            child: pw.Column(
              mainAxisAlignment: pw.MainAxisAlignment.center,
              children: [
                pw.Text('KaushalPass Digital Skill Passport', style: pw.TextStyle(fontSize: 24, fontWeight: pw.FontWeight.bold)),
                pw.SizedBox(height: 20),
                pw.Text('Name: ${user.name.isEmpty ? 'Unknown' : user.name}', style: const pw.TextStyle(fontSize: 18)),
                pw.Text('State: ${user.state}', style: const pw.TextStyle(fontSize: 18)),
                pw.Text('Occupation: ${user.occupation}', style: const pw.TextStyle(fontSize: 18)),
                pw.SizedBox(height: 40),
                pw.Text('Verified Skills:', style: pw.TextStyle(fontSize: 20, fontWeight: pw.FontWeight.bold)),
                pw.SizedBox(height: 10),
                pw.Text('- Bridal Mehendi (NSQF Level 4) - Verified by AI', style: const pw.TextStyle(fontSize: 16)),
                pw.Text('- Basic Tailoring (NSQF Level 2) - Community Verified', style: const pw.TextStyle(fontSize: 16)),
                pw.SizedBox(height: 40),
                pw.BarcodeWidget(
                  barcode: pw.Barcode.qrCode(),
                  data: 'https://kaushalpass.gov.in/verify/KP-2026-9812',
                  width: 150,
                  height: 150,
                ),
                pw.SizedBox(height: 20),
                pw.Text('Scan to Verify', style: const pw.TextStyle(fontSize: 14)),
              ],
            ),
          );
        },
      ),
    );

    await Printing.layoutPdf(
      onLayout: (PdfPageFormat format) async => pdf.save(),
    );
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final user = ref.watch(userProfileProvider);
    final displayName = user.name.isNotEmpty ? user.name : 'Unknown User';

    return Scaffold(
      backgroundColor: Colors.white,
      extendBodyBehindAppBar: true,
      appBar: AppBar(
        title: const Text('Digital Skill Passport', style: TextStyle(color: Colors.black87)),
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
              children: [
                Container(
                  padding: const EdgeInsets.all(32),
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(32),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withValues(alpha: 0.05),
                        blurRadius: 20,
                        offset: const Offset(0, 10),
                      )
                    ]
                  ),
                  child: Column(
                    children: [
                      Row(
                        children: [
                          Container(
                            decoration: BoxDecoration(
                              shape: BoxShape.circle,
                              border: Border.all(color: const Color(0xFF7C3AED), width: 2),
                            ),
                            child: const CircleAvatar(
                              radius: 32,
                              backgroundImage: NetworkImage('https://i.pravatar.cc/150?img=47'),
                            ),
                          ),
                          const SizedBox(width: 16),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(displayName, style: const TextStyle(color: Colors.black87, fontSize: 22, fontWeight: FontWeight.bold)),
                                Text('ID: KP-2026-9812', style: const TextStyle(color: Colors.black54, fontSize: 14)),
                              ],
                            ),
                          ),
                          const Icon(Icons.verified, color: Colors.blueAccent, size: 36),
                        ],
                      ),
                      const SizedBox(height: 40),
                      Container(
                        padding: const EdgeInsets.all(16),
                        decoration: BoxDecoration(
                          color: Colors.white,
                          borderRadius: BorderRadius.circular(20),
                          boxShadow: [
                            BoxShadow(color: Colors.black.withValues(alpha: 0.03), blurRadius: 10, offset: const Offset(0, 5))
                          ]
                        ),
                        child: QrImageView(
                          data: 'https://kaushalpass.gov.in/verify/KP-2026-9812',
                          version: QrVersions.auto,
                          size: 200.0,
                          eyeStyle: const QrEyeStyle(eyeShape: QrEyeShape.square, color: Color(0xFF7C3AED)),
                          dataModuleStyle: const QrDataModuleStyle(dataModuleShape: QrDataModuleShape.square, color: Colors.black87),
                        ),
                      ),
                      const SizedBox(height: 24),
                      const Text(
                        'Scan to Verify Skills',
                        style: TextStyle(color: Colors.black54, fontSize: 16, fontWeight: FontWeight.w600, letterSpacing: 1),
                      ),
                    ],
                  ),
                ).animate().fadeIn(duration: 600.ms).slideY(begin: -0.1, end: 0),
                
                const SizedBox(height: 40),
                const Align(
                  alignment: Alignment.centerLeft,
                  child: Text(
                    'Verified Skills',
                    style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Colors.black87),
                  ),
                ).animate().fadeIn(delay: 400.ms),
                const SizedBox(height: 16),
                
                ListView(
                  shrinkWrap: true,
                  physics: const NeverScrollableScrollPhysics(),
                  children: [
                    _buildSkillTile(context, 'Bridal Mehendi', 'NSQF Level 4', 'Verified by AI').animate().fadeIn(delay: 600.ms).slideX(begin: 0.2),
                    _buildSkillTile(context, 'Basic Tailoring', 'NSQF Level 2', 'Community Verified').animate().fadeIn(delay: 800.ms).slideX(begin: 0.2),
                  ],
                ),
                
                const SizedBox(height: 40),
                SizedBox(
                  width: double.infinity,
                  child: OutlinedButton.icon(
                    onPressed: () => _generateAndPrintPDF(user),
                    icon: const Icon(Icons.picture_as_pdf, color: Color(0xFF7C3AED)),
                    label: const Text('Download PDF Certificate'),
                    style: OutlinedButton.styleFrom(
                      foregroundColor: const Color(0xFF7C3AED),
                      side: const BorderSide(color: Color(0xFF7C3AED), width: 2),
                      padding: const EdgeInsets.symmetric(vertical: 20),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(20),
                      ),
                      textStyle: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                    ),
                  ),
                ).animate().fadeIn(delay: 1000.ms)
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildSkillTile(BuildContext context, String title, String level, String status) {
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(color: Colors.black.withValues(alpha: 0.05), blurRadius: 10, offset: const Offset(0, 5))
        ]
      ),
      child: ListTile(
        contentPadding: const EdgeInsets.all(16),
        title: Text(title, style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.black87, fontSize: 18)),
        subtitle: Padding(
          padding: const EdgeInsets.only(top: 8.0),
          child: Text('\$level • \$status', style: const TextStyle(color: Colors.black54)),
        ),
        trailing: Container(
          padding: const EdgeInsets.all(8),
          decoration: BoxDecoration(
            color: Colors.amber.withValues(alpha: 0.1),
            shape: BoxShape.circle,
          ),
          child: const Icon(Icons.star, color: Colors.amber),
        ),
      ),
    );
  }
}
