import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:hive_flutter/hive_flutter.dart';

class UserProfile {
  final String name;
  final String state;
  final String language;
  final String occupation;

  UserProfile({
    required this.name,
    required this.state,
    required this.language,
    required this.occupation,
  });

  factory UserProfile.empty() => UserProfile(name: '', state: '', language: '', occupation: '');

  UserProfile copyWith({String? name, String? state, String? language, String? occupation}) {
    return UserProfile(
      name: name ?? this.name,
      state: state ?? this.state,
      language: language ?? this.language,
      occupation: occupation ?? this.occupation,
    );
  }
}

class UserProfileNotifier extends Notifier<UserProfile> {
  final _box = Hive.box('credoraBox');

  @override
  UserProfile build() {
    return UserProfile(
      name: _box.get('name', defaultValue: ''),
      state: _box.get('state', defaultValue: ''),
      language: _box.get('language', defaultValue: 'English'),
      occupation: _box.get('occupation', defaultValue: ''),
    );
  }

  Future<void> updateProfile(UserProfile profile) async {
    await _box.put('name', profile.name);
    await _box.put('state', profile.state);
    await _box.put('language', profile.language);
    await _box.put('occupation', profile.occupation);
    state = profile;
  }
}

final userProfileProvider = NotifierProvider<UserProfileNotifier, UserProfile>(() {
  return UserProfileNotifier();
});
