import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:hive/hive.dart';
import '../data/user_provider.dart';
import '../../../core/localization/app_localizations.dart';

class ProfileScreen extends ConsumerWidget {
  const ProfileScreen({super.key});

  void _showLanguagePicker(BuildContext context, WidgetRef ref, String currentLang) {
    showModalBottomSheet(
      context: context,
      backgroundColor: Colors.white,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
      ),
      builder: (context) {
        return SafeArea(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const SizedBox(height: 16),
              Text(
                AppLocales.get('change_language', currentLang),
                style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.black87),
              ),
              const SizedBox(height: 16),
              ...['English', 'Hindi', 'Tamil', 'Telugu', 'Kannada', 'Bengali'].map((lang) {
                return ListTile(
                  title: Text(lang, style: TextStyle(color: lang == currentLang ? const Color(0xFF7C3AED) : Colors.black87)),
                  trailing: lang == currentLang ? const Icon(Icons.check, color: Color(0xFF7C3AED)) : null,
                  onTap: () async {
                    final user = ref.read(userProfileProvider);
                    await ref.read(userProfileProvider.notifier).updateProfile(
                      user.copyWith(language: lang)
                    );
                    if (context.mounted) Navigator.pop(context);
                  },
                );
              }),
              const SizedBox(height: 16),
            ],
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final user = ref.watch(userProfileProvider);

    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        title: Text(AppLocales.get('profile', user.language), style: const TextStyle(color: Colors.black87)),
        backgroundColor: Colors.transparent,
        elevation: 0,
        iconTheme: const IconThemeData(color: Colors.black87),
      ),
      body: Container(
        height: double.infinity,
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [Color(0xFFFFEAD2), Color(0xFFE6EFFF)],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
        ),
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            children: [
              const CircleAvatar(
                radius: 50,
                backgroundImage: NetworkImage('https://i.pravatar.cc/150?img=47'),
              ),
              const SizedBox(height: 16),
              Text(user.name.isEmpty ? 'Unknown User' : user.name, style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Colors.black87)),
              Text('ID: KP-2026-9812', style: const TextStyle(fontSize: 16, color: Colors.black54)),
              const SizedBox(height: 32),
              _buildProfileItem(Icons.location_on, AppLocales.get('state', user.language), user.state.isEmpty ? 'Not set' : user.state),
              _buildProfileItem(Icons.language, AppLocales.get('language', user.language), user.language, onTap: () => _showLanguagePicker(context, ref, user.language)),
              _buildProfileItem(Icons.work, AppLocales.get('occupation', user.language), user.occupation.isEmpty ? 'Not set' : user.occupation),
              const SizedBox(height: 40),
              SizedBox(
                width: double.infinity,
                child: FilledButton.icon(
                  onPressed: () async {
                    await Hive.box('credoraBox').clear();
                    if (context.mounted) {
                      context.go('/login');
                    }
                  },
                  icon: const Icon(Icons.logout, color: Colors.white),
                  label: Text(AppLocales.get('logout', user.language)),
                  style: FilledButton.styleFrom(
                    backgroundColor: Colors.redAccent,
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildProfileItem(IconData icon, String title, String value, {VoidCallback? onTap}) {
    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(color: Colors.black.withValues(alpha: 0.05), blurRadius: 10, offset: const Offset(0, 5))
        ]
      ),
      child: ListTile(
        leading: Icon(icon, color: const Color(0xFF7C3AED)),
        title: Text(title, style: const TextStyle(color: Colors.black54, fontSize: 14)),
        subtitle: Text(value, style: const TextStyle(color: Colors.black87, fontSize: 18, fontWeight: FontWeight.w500)),
        trailing: onTap != null ? const Icon(Icons.edit, color: Colors.black26) : null,
        onTap: onTap,
      ),
    );
  }
}
