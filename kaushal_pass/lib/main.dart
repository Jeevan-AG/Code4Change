import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:google_fonts/google_fonts.dart';
import 'core/router/app_router.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Initialize Hive for offline support
  await Hive.initFlutter();
  await Hive.openBox('kaushalBox');

  // Supabase initialization would go here
  // await Supabase.initialize(...);

  runApp(
    const ProviderScope(
      child: KaushalPassApp(),
    ),
  );
}

class KaushalPassApp extends ConsumerWidget {
  const KaushalPassApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final router = ref.watch(appRouterProvider);
    return MaterialApp.router(
      title: 'KaushalPass',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF7C3AED), // Deep violet primary color
          brightness: Brightness.light,
          primary: const Color(0xFF7C3AED),
          secondary: const Color(0xFFFF9800),
          surface: Colors.white,
        ),
        textTheme: GoogleFonts.outfitTextTheme(), // Modern, clean typography
        useMaterial3: true,
      ),
      routerConfig: router,
    );
  }
}
