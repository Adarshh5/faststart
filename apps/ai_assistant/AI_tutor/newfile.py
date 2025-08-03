from langchain_core.documents import Document

import faiss    

from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from dotenv import load_dotenv
load_dotenv() 

import os

os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")


documents = [
    Document(
        page_content="Q: I feel bored talking to AI every day, what should I do?\nA: It's totally normal to feel bored sometimes. Try changing the topic based on your interest like movies, goals, daily life, or even jokes. Treat AI like a friend and have casual conversations—it will feel fresh and fun.",
        metadata={
            "question": "I feel bored talking to AI every day, what should I do?",
            "answer": "It's totally normal to feel bored sometimes. Try changing the topic based on your interest like movies, goals, daily life, or even jokes. Treat AI like a friend and have casual conversations—it will feel fresh and fun.",
            "source": "motivation"
        }
    ),
    Document(
        page_content="Q: Can I talk to AI in Hindi too?\nA: Yes, you can! But if your goal is to improve English, use a mix of Hindi and English in the beginning. Slowly, you will start using more English naturally without forcing it.",
        metadata={
            "question": "Can I talk to AI in Hindi too?",
            "answer": "Yes, you can! But if your goal is to improve English, use a mix of Hindi and English in the beginning. Slowly, you will start using more English naturally without forcing it.",
            "source": "learning_support"
        }
    ),
    Document(
        page_content="Q: What if I make grammar mistakes while talking to AI?\nA: Don’t worry about mistakes, that’s how you learn. When you make a mistake, just ask AI to correct it. This way you improve your grammar and confidence both at the same time, and with time you will automatically not make grammar mistake if you practice every day.",
        metadata={
            "question": "What if I make grammar mistakes while talking to AI?",
            "answer": "Don’t worry about mistakes, that’s how you learn. When you make a mistake, just ask AI to correct it. This way you improve your grammar and confidence both at the same time, and with time you will automatically not make grammar mistake if you practice every day.",
            "source": "learning_support"
        }
    ),
    Document(
        page_content="Q: I often forget words while speaking, what should I do?\nA: It’s okay to forget. Try using a similar word or describe what you want to say. Also, learn vocabulary and write your own definitions—that helps you remember them better.",
        metadata={
            "question": "I often forget words while speaking, what should I do?",
            "answer": "It’s okay to forget. Try using a similar word or describe what you want to say. Also, learn vocabulary and write your own definitions—that helps you remember them better.",
            "source": "learning_support"
        }
    ),
    
    Document(
        page_content="Q: How can I increase my speaking time with AI?\nA: Start small—maybe 10 minutes a day. Slowly increase it to 30 minutes or more. Make a list of topics or ask AI to give you one. When you enjoy the topic, time will pass easily.",
        metadata={
            "question": "How can I increase my speaking time with AI?",
            "answer": "Start small—maybe 10 minutes a day. Slowly increase it to 30 minutes or more. Make a list of topics or ask AI to give you one. When you enjoy the topic, time will pass easily.",
            "source": "practice_routine"
        }
    ),
    Document(
        page_content="Q: How do I start thinking in English?\nA: Start with daily actions. Think in English about what you’re doing—like eating, walking, working. Try writing your own definitions in English too in word definition box. In 1–2 months, thinking in English will feel natural.",
        metadata={
            "question": "How do I start thinking in English?",
            "answer": "Start with daily actions. Think in English about what you’re doing—like eating, walking, working. Try writing your own definitions in English too in word definition box. In 1–2 months, thinking in English will feel natural.",
            "source": "motivation"
        }
    ),
    Document(
        page_content="Q: How do I understand new words used in AI responses?\nA: Ask AI what the word means or how to use it in a sentence. You can also save the word so AI uses it more often in your chats. That way, you’ll learn it without even realizing.",
        metadata={
            "question": "How do I understand new words used in AI responses?",
            "answer": "Ask AI what the word means or how to use it in a sentence. You can also save the word so AI uses it more often in your chats. That way, you’ll learn it without even realizing.",
            "source": "learning_support"
        }
    ),
    Document(
        page_content="Q: How should I decide which word to learn?\nA: You don’t need to decide manually. Words are already organized from beginner to advanced. Just skip the words you already know and focus only on the new ones you don’t understand.",
        metadata={
            "question": "How should I decide which word to learn?",
            "answer": "You don’t need to decide manually. Words are already organized from beginner to advanced. Just skip the words you already know and focus only on the new ones you don’t understand.",
            "source": "learning_support"
        }
    ),
    Document(
        page_content="Q: Will AI give me new words every day?\nA: Yes, but only if you ask. You can simply say “Give me 5 new words today” and AI will help you learn fresh vocabulary daily.",
        metadata={
            "question": "Will AI give me new words every day?",
            "answer": "Yes, but only if you ask. You can simply say “Give me 5 new words today” and AI will help you learn fresh vocabulary daily.",
            "source": "learning_support"
        }
    ),
    Document(
        page_content="Q: When does the learned vocabulary get repeated?\nA: Your saved words are repeated naturally when you talk to the AI or read AI-generated content. This helps you remember and use them without extra effort.",
        metadata={
            "question": "When does the learned vocabulary get repeated?",
            "answer": "Your saved words are repeated naturally when you talk to the AI or read AI-generated content. This helps you remember and use them without extra effort.",
            "source": "learning_support"
        }
    ),
    Document(
        page_content="Q: What if I forget a word I already learned?\nA: Don’t worry, AI will keep using your saved words in chats, so it’s hard to forget them. But if you do, just review your saved words anytime to refresh your memory.",
        metadata={
            "question": "What if I forget a word I already learned?",
            "answer": "Don’t worry, AI will keep using your saved words in chats, so it’s hard to forget them. But if you do, just review your saved words anytime to refresh your memory.",
            "source": "learning_support"
        }
    ),
    Document(
        page_content="Q: Are 5 words a day enough or should I learn more?\nA: 5 words a day are enough if you stay consistent. If you have more time and feel comfortable, you can increase to 10 words—but focus on understanding, not just memorizing.",
        metadata={
            "question": "Are 5 words a day enough or should I learn more?",
            "answer": "5 words a day are enough if you stay consistent. If you have more time and feel comfortable, you can increase to 10 words—but focus on understanding, not just memorizing.",
            "source": "learning_support"
        }
    ),
    Document(
        page_content="Q: Is it necessary to make sentences while learning vocabulary?\nA: Yes, making sentences is very helpful. It trains your brain to think in English and shows you how to use the word in real situations.",
        metadata={
            "question": "Is it necessary to make sentences while learning vocabulary?",
            "answer": "Yes, making sentences is very helpful. It trains your brain to think in English and shows you how to use the word in real situations.",
            "source": "learning_support"
        }
    ),
    Document(
        page_content="Q: Will AI use only the words I have learned?\nA: Not only those, but AI will try to include your saved words more often in conversation. This helps you see them in context while keeping the chat friendly and natural.",
        metadata={
            "question": "Will AI use only the words I have learned?",
            "answer": "Not only those, but AI will try to include your saved words more often in conversation. This helps you see them in context while keeping the chat friendly and natural.",
            "source": "learning_support"
        }
    ),
    Document(
        page_content="Q: What happens when I click the delete button?\nA: If you click the delete button, that word is removed from your saved list. AI will stop using it in your responses, so only keep the words you want to keep practicing.",
        metadata={
            "question": "What happens when I click the delete button?",
            "answer": "If you click the delete button, that word is removed from your saved list. AI will stop using it in your responses, so only keep the words you want to keep practicing.",
            "source": "app_info"
        }
    ),
    Document(
        page_content="Q: How can I give feedback in the app?\nA: Just go to the feedback page inside the app. There you can share your suggestions or problems directly with us.",
        metadata={
            "question": "How can I give feedback in the app?",
            "answer": "Just go to the feedback page inside the app. There you can share your suggestions or problems directly with us.",
            "source": "app_info"
        }
    ),
    Document(
        page_content="Q: Can I talk to AI on a specific topic?\nA: Yes, you can! Just ask AI to talk about any topic you like—movies, tech, your goals, or daily life. It will adjust to your topic instantly.",
        metadata={
            "question": "Can I talk to AI on a specific topic?",
            "answer": "Yes, you can! Just ask AI to talk about any topic you like—movies, tech, your goals, or daily life. It will adjust to your topic instantly.",
            "source": "practice_routine"
        }
    ),
    Document(
        page_content="Q: Can AI give me a speaking test?\nA: Yes, you can ask AI to take a speaking test. It can ask you questions, give feedback, and even help you improve your fluency step-by-step.",
        metadata={
            "question": "Can AI give me a speaking test?",
            "answer": "Yes, you can ask AI to take a speaking test. It can ask you questions, give feedback, and even help you improve your fluency step-by-step.",
            "source": "practice_routine"
        }
    ),
    Document(
        page_content="Q: What should I do if I have a doubt in AI’s answer?\nA: Just ask! You can say, “Can you explain again?” or “Please make it simpler.” AI is here to help you until you understand clearly.",
        metadata={
            "question": "What should I do if I have a doubt in AI’s answer?",
            "answer": "Just ask! You can say, “Can you explain again?” or “Please make it simpler.” AI is here to help you until you understand clearly.",
            "source": "learning_support"
        }
    ),
    Document(
        page_content="Q: Do I also need coaching with this app?\nA: No, you don’t. The app is designed to give you everything you need for practical spoken English—no extra coaching needed.",
        metadata={
            "question": "Do I also need coaching with this app?",
            "answer": "No, you don’t. The app is designed to give you everything you need for practical spoken English—no extra coaching needed.",
            "source": "app_info"
        }
    ),
    Document(
        page_content="Q: Can school or college students use this app?\nA: Yes, of course! This app is perfect for students who want to improve their English in a simple and smart way.",
        metadata={
            "question": "Can school or college students use this app?",
            "answer": "Yes, of course! This app is perfect for students who want to improve their English in a simple and smart way.",
            "source": "use_cases"
        }
    ),
    Document(
        page_content="Q: Will this app help in interview preparation?\nA: Yes, especially for spoken part. It helps you answer fluently, talk with confidence, and build the right vocabulary for interviews.",
        metadata={
            "question": "Will this app help in interview preparation?",
            "answer": "Yes, especially for spoken part. It helps you answer fluently, talk with confidence, and build the right vocabulary for interviews.",
            "source": "use_cases"
        }
    ),
    Document(
        page_content="Q: Can I use this app for IELTS or TOEFL preparation?\nA: Maybe, but mainly it's focused on spoken English. If speaking is your weak area, this app will be super helpful for that.",
        metadata={
            "question": "Can I use this app for IELTS or TOEFL preparation?",
            "answer": "Maybe, but mainly it's focused on spoken English. If speaking is your weak area, this app will be super helpful for that.",
            "source": "use_cases"
        }
    ),
    Document(
        page_content="Q: Do I need to study with a teacher too?\nA: No, you don’t. The app works like a personal guide and gives you practice every day without needing a teacher.",
        metadata={
            "question": "Do I need to study with a teacher too?",
            "answer": "No, you don’t. The app works like a personal guide and gives you practice every day without needing a teacher.",
            "source": "app_info"
        }
    ),
    Document(
        page_content="Q: Is this app like a spoken course?\nA: No, it’s better than a course. It’s 100% practical and focused on real conversations, which makes learning faster and natural.",
        metadata={
            "question": "Is this app like a spoken course?",
            "answer": "No, it’s better than a course. It’s 100% practical and focused on real conversations, which makes learning faster and natural.",
            "source": "app_info"
        }
    ),
    Document(
        page_content="Q: What else should I study along with this app?\nA: Nothing extra is needed. Just stay consistent with this app and keep practicing every day—that’s enough to improve your English.",
        metadata={
            "question": "What else should I study along with this app?",
            "answer": "Nothing extra is needed. Just stay consistent with this app and keep practicing every day—that’s enough to improve your English.",
            "source": "app_info"
        }
    ),
    Document(
        page_content="Q: Can AI give me practice questions?\nA: Yes! You can ask for practice questions anytime—related to vocabulary, grammar, speaking, or any topic you want.",
        metadata={
            "question": "Can AI give me practice questions?",
            "answer": "Yes! You can ask for practice questions anytime—related to vocabulary, grammar, speaking, or any topic you want.",
            "source": "practice_routine"
        }
    ),
    Document(
        page_content="Q: Does this app work offline?\nA: No, the app needs internet to work because AI needs real-time data to chat and respond.",
        metadata={
            "question": "Does this app work offline?",
            "answer": "No, the app needs internet to work because AI needs real-time data to chat and respond.",
            "source": "app_info"
        }
    ),
    Document(
        page_content="Q: Will this app have video chat in the future?\nA: No, this app is focused only on text-based speaking practice. Video chat is not part of the plan right now.",
        metadata={
            "question": "Will this app have video chat in the future?",
            "answer": "No, this app is focused only on text-based speaking practice. Video chat is not part of the plan right now.",
            "source": "app_info"
        }
    ),
    Document(
        page_content="Q: What should I do when I don’t feel like studying?\nA: On those days, just talk to AI casually. Share your thoughts, mood, or random things—this way you stay in practice without pressure.",
        metadata={
            "question": "What should I do when I don’t feel like studying?",
            "answer": "On those days, just talk to AI casually. Share your thoughts, mood, or random things—this way you stay in practice without pressure.",
            "source": "motivation"
        }
    ),
    Document(
        page_content="Q: Should I fix a specific time for daily practice?\nA: Yes, setting a fixed time helps build a habit. Even 15–30 minutes daily at the same time can make a big difference.",
        metadata={
            "question": "Should I fix a specific time for daily practice?",
            "answer": "Yes, setting a fixed time helps build a habit. Even 15–30 minutes daily at the same time can make a big difference.",
            "source": "practice_routine"
        }
    ),
    Document(
        page_content="Q: I can’t even give 30 minutes daily. Is that okay?\nA: That’s okay! Even 10–15 minutes is better than nothing. The key is daily practice, not how long you spend.",
        metadata={
            "question": "I can’t even give 30 minutes daily. Is that okay?",
            "answer": "That’s okay! Even 10–15 minutes is better than nothing. The key is daily practice, not how long you spend.",
            "source": "practice_routine"
        }
    ),
    Document(
        page_content="Q: If I stop in between, will I lose all progress?\nA: No, you won’t lose your progress. But regular practice keeps your mind active, so try to stay consistent even if it’s a short time.",
        metadata={
            "question": "If I stop in between, will I lose all progress?",
            "answer": "No, you won’t lose your progress. But regular practice keeps your mind active, so try to stay consistent even if it’s a short time.",
            "source": "motivation"
        }
    ),
    Document(
        page_content="Q: I feel guilty when I miss practice. What should I do?\nA: Don’t feel guilty. Just continue the next day without pressure. Guilt stops progress, but small consistent steps build confidence.",
        metadata={
            "question": "I feel guilty when I miss practice. What should I do?",
            "answer": "Don’t feel guilty. Just continue the next day without pressure. Guilt stops progress, but small consistent steps build confidence.",
            "source": "motivation"
        }
    ),
    Document(
        page_content="Q: Can the app give features for motivation?\nA: Yes! The app gives you interesting topics, achievements, and goals to keep you motivated and engaged every day.",
        metadata={
            "question": "Can the app give features for motivation?",
            "answer": "Yes! The app gives you interesting topics, achievements, and goals to keep you motivated and engaged every day.",
            "source": "app_info"
        }
    ),
    Document(
        page_content="Q: How do I set my learning goals?\nA: Start with small goals—like “5 new words a day” or “10 minutes speaking daily.” As you improve, set higher goals and track your progress.",
        metadata={
            "question": "How do I set my learning goals?",
            "answer": "Start with small goals—like “5 new words a day” or “10 minutes speaking daily.” As you improve, set higher goals and track your progress.",
            "source": "practice_routine"
        }
    ),
    Document(
        page_content="Q: Can AI motivate me?\nA: Yes! Just tell AI when you’re feeling low or unmotivated. It can share quotes, reminders, and friendly encouragement to keep you going.",
        metadata={
            "question": "Can AI motivate me?",
            "answer": "Yes! Just tell AI when you’re feeling low or unmotivated. It can share quotes, reminders, and friendly encouragement to keep you going.",
            "source": "motivation"
        }
    ),
    Document(
        page_content="Q: Should I record myself speaking in English?\nA: No need to record. Just keep speaking with AI every day. That’s enough to improve fluency and confidence without any extra tools.",
        metadata={
            "question": "Should I record myself speaking in English?",
            "answer": "No need to record. Just keep speaking with AI every day. That’s enough to improve fluency and confidence without any extra tools.",
            "source": "practice_routine"
        }
    ),
    Document(
        page_content="Q: Is it better to practice with a friend too?\nA: Yes, absolutely! If you can, invite a friend and practice together. Talking with someone at your level helps you grow faster.",
        metadata={
            "question": "Is it better to practice with a friend too?",
            "answer": "Yes, absolutely! If you can, invite a friend and practice together. Talking with someone at your level helps you grow faster.",
            "source": "practice_routine"
        }
    ),

    Document(
        page_content="Q: I don’t understand AI’s pronunciation. What should I do?\nA: It’s totally normal in the beginning. Just keep practicing and listening daily—within a few weeks, your ears will adjust naturally.",
        metadata={
            "question": "I don’t understand AI’s pronunciation. What should I do?",
            "answer": "It’s totally normal in the beginning. Just keep practicing and listening daily—within a few weeks, your ears will adjust naturally.",
            "source": "learning_support"
        }
    ),
    Document(
        page_content="Q: Will the app have a voice feature in the future?\nA: It already has a voice feature! You can listen to pronunciation and use voice input for a better learning experience.",
        metadata={
            "question": "Will the app have a voice feature in the future?",
            "answer": "It already has a voice feature! You can listen to pronunciation and use voice input for a better learning experience.",
            "source": "app_info"
        }
    ),
    Document(
        page_content="Q: Can pronunciation be learned without speaking?\nA: No, to improve pronunciation you need to speak out loud. Listening helps, but speaking is the only way to train your tongue and muscles.",
        metadata={
            "question": "Can pronunciation be learned without speaking?",
            "answer": "No, to improve pronunciation you need to speak out loud. Listening helps, but speaking is the only way to train your tongue and muscles.",
            "source": "learning_support"
        }
    ),
    Document(
        page_content="Q: Can I check if I’m pronouncing correctly?\nA: Not yet. The app doesn't check your voice accuracy right now. But with enough listening and repeating, you’ll improve on your own.",
        metadata={
            "question": "Can I check if I’m pronouncing correctly?",
            "answer": "Not yet. The app doesn't check your voice accuracy right now. But with enough listening and repeating, you’ll improve on your own.",
            "source": "app_info"
        }
    ),
    Document(
        page_content="Q: Will AI teach me how to pronounce words correctly?\nA: Yes, AI can pronounce any word for you and give example sentences so you can copy the correct sound and practice it daily.",
        metadata={
            "question": "Will AI teach me how to pronounce words correctly?",
            "answer": "Yes, AI can pronounce any word for you and give example sentences so you can copy the correct sound and practice it daily.",
            "source": "learning_support"
        }
    ),
    Document(
        page_content="Q: Does AI support voice commands?\nA: Yes, the app supports voice commands. You can speak instead of typing, making the practice more natural and hands-free.",
        metadata={
            "question": "Does AI support voice commands?",
            "answer": "Yes, the app supports voice commands. You can speak instead of typing, making the practice more natural and hands-free.",
            "source": "app_info"
        }
    ),
    Document(
        page_content="Q: Does the app provide listening exercises?\nA: Yes, listening is the second main feature of the app. It helps you understand native-like pronunciation and improves comprehension.",
        metadata={
            "question": "Does the app provide listening exercises?",
            "answer": "Yes, listening is the second main feature of the app. It helps you understand native-like pronunciation and improves comprehension.",
            "source": "app_info"
        }
    ),
    Document(
        page_content="Q: How can I get used to English sounds?\nA: Just practice listening every day, even if it’s only 10 to 20 minutes. Over time, you’ll start recognizing sounds and words faster.",
        metadata={
            "question": "How can I get used to English sounds?",
            "answer": "Just practice listening every day, even if it’s only 10 to 20 minutes. Over time, you’ll start recognizing sounds and words faster.",
            "source": "practice_routine"
        }
    ),
    Document(
        page_content="Q: Should I practice using headphones?\nA: Yes, if you have headphones, definitely use them. They help you catch clear pronunciation and reduce background noise.",
        metadata={
            "question": "Should I practice using headphones?",
            "answer": "Yes, if you have headphones, definitely use them. They help you catch clear pronunciation and reduce background noise.",
            "source": "practice_routine"
        }
    ),
    Document(
        page_content="Q: If I speak incorrectly, will AI correct me?\nA: No, AI won’t interrupt or correct every mistake during conversation. The goal is to keep you motivated and make practice smooth.",
        metadata={
            "question": "If I speak incorrectly, will AI correct me?",
            "answer": "No, AI won’t interrupt or correct every mistake during conversation. The goal is to keep you motivated and make practice smooth.",
            "source": "learning_support"
        }
    ),
    Document(
        page_content="Q: Can the app suggest areas for improvement?\nA: Right now, this feature is not available. But in future updates, we plan to add personalized improvement suggestions.",
        metadata={
            "question": "Can the app suggest areas for improvement?",
            "answer": "Right now, this feature is not available. But in future updates, we plan to add personalized improvement suggestions.",
            "source": "app_info"
        }
    ),
    Document(
        page_content="Q: Can AI give me grammar tests?\nA: Yes, you can ask for grammar tests anytime. AI can quiz you on tenses, sentence structure, and more to build your understanding.",
        metadata={
            "question": "Can AI give me grammar tests?",
            "answer": "Yes, you can ask for grammar tests anytime. AI can quiz you on tenses, sentence structure, and more to build your understanding.",
            "source": "learning_support"
        }
    ),
    Document(
        page_content="Q: Can I solve exam questions with AI?\nA: Yes, you can ask AI to solve exam-style questions. It will help you understand the logic and learn better ways to answer.",
        metadata={
            "question": "Can I solve exam questions with AI?",
            "answer": "Yes, you can ask AI to solve exam-style questions. It will help you understand the logic and learn better ways to answer.",
            "source": "learning_support"
        }
    ),
    Document(
        page_content="Q: Will the app have a doubt-solving session?\nA: Yes! The app has a dedicated doubt-solving chatbot. You can ask anything you don’t understand and get a clear explanation.",
        metadata={
            "question": "Will the app have a doubt-solving session?",
            "answer": "Yes! The app has a dedicated doubt-solving chatbot. You can ask anything you don’t understand and get a clear explanation.",
            "source": "app_info"
        }
    ),
    Document(
        page_content="Q: Can AI give me speaking feedback?\nA: Right now, AI doesn’t give direct feedback on your voice or pronunciation. But future updates may include more feedback tools.",
        metadata={
            "question": "Can AI give me speaking feedback?",
            "answer": "Right now, AI doesn’t give direct feedback on your voice or pronunciation. But future updates may include more feedback tools.",
            "source": "app_info"
        }
    ),
    Document(
        page_content="Q: Can I do roleplays with AI like job interviews or shopping?\nA: Yes, absolutely! You can ask AI to do roleplays for situations like interviews, shops, or phone calls. It's great for real-world practice.",
        metadata={
            "question": "Can I do roleplays with AI like job interviews or shopping?",
            "answer": "Yes, absolutely! You can ask AI to do roleplays for situations like interviews, shops, or phone calls. It's great for real-world practice.",
            "source": "practice_routine"
        }
    ),
    Document(
        page_content="Q: Is the grammar provided enough for spoken English?\nA: The grammar provided is enough to get started with spoken English. There are more grammar rules, but as you practice daily, you'll naturally begin to understand and use them. Around 90% of spoken English relies on basic grammar. The main goal is to help you understand the time frame of a sentence—whether it's in the past, present, or future—and the overall sense.",
        metadata={
            "question": "Is the grammar provided enough for spoken English?",
            "answer": "The grammar provided is enough to get started with spoken English. There are more grammar rules, but as you practice daily, you'll naturally begin to understand and use them. Around 90% of spoken English relies on basic grammar. The main goal is to help you understand the time frame of a sentence—whether it's in the past, present, or future—and the overall sense.",
            "source": "learning_support"
        }
    ),
    Document(
        page_content="Q: Where should I practice grammar for spoken English?\nA: You don’t need to do extra grammar practice for spoken English. Just a basic understanding is enough to begin. The grammar we’ve covered in the grammar section is sufficient for day-to-day conversations. You don’t need to memorize grammar rules—just focus on understanding the concept and meaning of each sentence.",
        metadata={
            "question": "Where should I practice grammar for spoken English?",
            "answer": "You don’t need to do extra grammar practice for spoken English. Just a basic understanding is enough to begin. The grammar we’ve covered in the grammar section is sufficient for day-to-day conversations. You don’t need to memorize grammar rules—just focus on understanding the concept and meaning of each sentence.",
            "source": "learning_support"
        }
    ),
    Document(
        page_content="Q: How does AI use these grammar concepts?\nA: When you study a grammar concept and mark it as complete, AI assumes you've learned it and tries to use it more often in its responses. This helps you revise the concept automatically without spending extra time. It also makes AI responses easier to understand since you’ve already studied those concepts.",
        metadata={
            "question": "How does AI use these grammar concepts?",
            "answer": "When you study a grammar concept and mark it as complete, AI assumes you've learned it and tries to use it more often in its responses. This helps you revise the concept automatically without spending extra time. It also makes AI responses easier to understand since you’ve already studied those concepts.",
            "source": "app_info"
        }
    ),
    Document(
        page_content="Q: How much vocabulary should I learn each day, and how much time should I spend on it?\nA: You should learn 5 to 10 new vocabulary words each day using our website. Try to dedicate 10 to 15 minutes daily to vocabulary learning.",
        metadata={
            "question": "How much vocabulary should I learn each day, and how much time should I spend on it?",
            "answer": "You should learn 5 to 10 new vocabulary words each day using our website. Try to dedicate 10 to 15 minutes daily to vocabulary learning.",
            "source": "practice_routine"
        }
    ),
    Document(
        page_content="Q: What should I do so I don't forget vocabulary?\nA: Try writing your own definitions for the words you learn—it helps with retention. And don’t worry if you forget words—AI will try to use the vocabulary you’ve studied in its responses, so the words will naturally become familiar over time.",
        metadata={
            "question": "What should I do so I don't forget vocabulary?",
            "answer": "Try writing your own definitions for the words you learn—it helps with retention. And don’t worry if you forget words—AI will try to use the vocabulary you’ve studied in its responses, so the words will naturally become familiar over time.",
            "source": "learning_support"
        }
    ),
    Document(
        page_content="Q: I already know many vocabulary words. Why should I learn from your list?\nA: If you already know a word, there’s no need to learn it again—it would just waste your time. You also don’t need to click the save button for known words because AI uses saved words in its responses. If you already know it, you don’t need to save it.",
        metadata={
            "question": "I already know many vocabulary words. Why should I learn from your list?",
            "answer": "If you already know a word, there’s no need to learn it again—it would just waste your time. You also don’t need to click the save button for known words because AI uses saved words in its responses. If you already know it, you don’t need to save it.",
            "source": "learning_support"
        }
    ),
    Document(
        page_content="Q: Which part of speech should I focus on more?\nA: You should study all parts of speech a little—like verbs, adjectives, adverbs, nouns, pronouns, and phrasal verbs. The good news is that we’ve provided a mix of everything, so you don’t need to search elsewhere.",
        metadata={
            "question": "Which part of speech should I focus on more?",
            "answer": "You should study all parts of speech a little—like verbs, adjectives, adverbs, nouns, pronouns, and phrasal verbs. The good news is that we’ve provided a mix of everything, so you don’t need to search elsewhere.",
            "source": "learning_support"
        }
    ),
    Document(
        page_content="Q: How much time should I talk with AI every day?\nA: You should chat with AI as much as your schedule allows, but try to speak for at least 30 minutes daily to build confidence.",
        metadata={
            "question": "How much time should I talk with AI every day?",
            "answer": "You should chat with AI as much as your schedule allows, but try to speak for at least 30 minutes daily to build confidence.",
            "source": "practice_routine"
        }
    ),
    Document(
        page_content="Q: What should I do if I don’t understand AI’s responses?\nA: Keep practicing daily even if you don’t understand anything at first. Within two months, you’ll start to understand some parts and learn vocabulary that will help you improve faster.",
        metadata={
            "question": "What should I do if I don’t understand AI’s responses?",
            "answer": "Keep practicing daily even if you don’t understand anything at first. Within two months, you’ll start to understand some parts and learn vocabulary that will help you improve faster.",
            "source": "practice_routine"
        }
    ),
    Document(
        page_content="Q: How do I think of new topics to chat about?\nA: Talk about your field of interest, your daily experiences, or situations you encounter. When you have free time, try to brainstorm topics—ideas will come naturally.",
        metadata={
            "question": "How do I think of new topics to chat about?",
            "answer": "Talk about your field of interest, your daily experiences, or situations you encounter. When you have free time, try to brainstorm topics—ideas will come naturally.",
            "source": "practice_routine"
        }
    ),
    Document(
        page_content="Q: I can’t even write a single sentence in English. Should I still start speaking practice?\nA: Yes, absolutely. Start speaking practice even if you can’t write a full sentence. Try using one or two English words in your sentences. Over time, you’ll naturally start using more English words in chats. Don’t feel nervous—just start practicing.",
        metadata={
            "question": "I can’t even write a single sentence in English. Should I still start speaking practice?",
            "answer": "Yes, absolutely. Start speaking practice even if you can’t write a full sentence. Try using one or two English words in your sentences. Over time, you’ll naturally start using more English words in chats. Don’t feel nervous—just start practicing.",
            "source": "motivation"
        }
    ),
    Document(
        page_content="Q: What happens if I click the delete button in the saved words section?\nA: If you delete a word, it means you don’t want the AI to use that word in its responses. You should delete words that you’ve already learned and started using so you can focus on new vocabulary instead of revisiting what you’ve already mastered.",
        metadata={
            "question": "What happens if I click the delete button in the saved words section?",
            "answer": "If you delete a word, it means you don’t want the AI to use that word in its responses. You should delete words that you’ve already learned and started using so you can focus on new vocabulary instead of revisiting what you’ve already mastered.",
            "source": "app_info"
        }
    ),
    Document(
        page_content="Q: Which words are mostly used by AI in its responses?\nA: AI mostly uses the words that you’ve currently saved in your vocabulary list.",
        metadata={
            "question": "Which words are mostly used by AI in its responses?",
            "answer": "AI mostly uses the words that you’ve currently saved in your vocabulary list.",
            "source": "app_info"
        }
    ),
    Document(
        page_content="Q: I got an error when clicking the detail button on some saved words. Why?\nA: That word has been removed from our database, so it’s no longer available in your vocabulary list.",
        metadata={
            "question": "I got an error when clicking the detail button on some saved words. Why?",
            "answer": "That word has been removed from our database, so it’s no longer available in your vocabulary list.",
            "source": "app_info"
        }
    ),
    Document(
        page_content="Q: Why should I share this app with my friends or relatives?\nA: Sharing the app makes your English-speaking journey more fun and faster. If your friends are at a similar learning stage, you can practice with them. Learning with a partner is one of the most effective ways to improve quickly.",
        metadata={
            "question": "Why should I share this app with my friends or relatives?",
            "answer": "Sharing the app makes your English-speaking journey more fun and faster. If your friends are at a similar learning stage, you can practice with them. Learning with a partner is one of the most effective ways to improve quickly.",
            "source": "motivation"
        }
    )
    
]





# embedding_model = OllamaEmbeddings(model='nomic-embed-text')
# vectorstore = FAISS.from_documents(documents, embedding_model)

# vectorstore.save_local('vector_db/')

from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import os


# embedding_model = OpenAIEmbeddings(model='text-embedding-3-small')  # Or 'text-embedding-3-large'
# vectorstore = FAISS.from_documents(documents, embedding_model)
# vectorstore.save_local('vector_db/')
from langchain_openai import OpenAIEmbeddings
embedder = OpenAIEmbeddings()
vector = embedder.embed_query("this is a test")
print(len(vector))
