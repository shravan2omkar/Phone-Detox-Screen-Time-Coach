import 'package:flutter/material.dart';
import 'dart:async';
import 'package:shared_preferences/shared_preferences.dart';

void main() => runApp(PhoneDetoxApp());

class PhoneDetoxApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Phone Detox Coach',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: DetoxHomePage(),
    );
  }
}

class DetoxHomePage extends StatefulWidget {
  @override
  _DetoxHomePageState createState() => _DetoxHomePageState();
}

class _DetoxHomePageState extends State<DetoxHomePage> {
  DateTime? startTime;
  int limitMinutes = 30;
  String sessionMessage = "";
  List<String> activities = [
    "📖 Read a book",
    "🚶 Go for a walk",
    "🧘 Try a breathing exercise",
    "🎨 Draw or doodle",
    "📓 Journal your thoughts",
    "📞 Call a friend"
  ];

  void startSession() {
    setState(() {
      startTime = DateTime.now();
      sessionMessage = "Session started. Stay mindful!";
    });
  }

  void endSession() {
    if (startTime != null) {
      final duration = DateTime.now().difference(startTime!).inMinutes;
      final exceeded = duration > limitMinutes;
      setState(() {
        sessionMessage =
            "Session ended. Duration: $duration minutes.\n" +
            (exceeded ? "⚠️ You exceeded your limit!" : "✅ Great job!");
        startTime = null;
      });
      saveSession(duration);
    } else {
      setState(() {
        sessionMessage = "No session in progress.";
      });
    }
  }

  void setLimit() async {
    final prefs = await SharedPreferences.getInstance();
    final newLimit = await showDialog<int>(
      context: context,
      builder: (context) => AlertDialog(
        title: Text("Set Time Limit"),
        content: TextField(
          keyboardType: TextInputType.number,
          decoration: InputDecoration(hintText: "Enter limit in minutes"),
          onSubmitted: (value) => Navigator.pop(context, int.tryParse(value)),
        ),
      ),
    );
    if (newLimit != null) {
      setState(() {
        limitMinutes = newLimit;
      });
      prefs.setInt('limitMinutes', newLimit);
    }
  }

  void suggestActivity() {
    final suggestion = (activities..shuffle()).first;
    setState(() {
      sessionMessage = "Try this: $suggestion";
    });
  }

  void saveSession(int duration) async {
    final prefs = await SharedPreferences.getInstance();
    final logs = prefs.getStringList('sessionLogs') ?? [];
    logs.add("${DateTime.now()}: $duration minutes");
    prefs.setStringList('sessionLogs', logs);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Phone Detox Coach")),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          children: [
            ElevatedButton(onPressed: startSession, child: Text("Start Session")),
            ElevatedButton(onPressed: endSession, child: Text("End Session")),
            ElevatedButton(onPressed: setLimit, child: Text("Set Time Limit")),
            ElevatedButton(onPressed: suggestActivity, child: Text("Suggest Offline Activity")),
            SizedBox(height: 20),
            Text(sessionMessage, style: TextStyle(fontSize: 16)),
          ],
        ),
      ),
    );
  }
}