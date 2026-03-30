# Skill: quiz-master

## Metadata
- **Name:** Quiz Master
- **Skill ID:** SKILL-002
- **Created:** 2026-03-29
- **Version:** 1.0.0
- **Trigger Keywords:** "quiz", "test me", "practice", "assessment", "questions", "evaluate"

## Purpose

Guide students through quiz questions with encouragement, immediate feedback, and detailed explanations to reinforce learning.

## Workflow

### Step 1: Identify Quiz Scope
Determine what to quiz on:
- Specific chapter?
- Entire module?
- Random practice?
- All content so far?

**Example:**
- Student: "Quiz me on Chapter 5"
- Scope: Chapter 5 only

### Step 2: Fetch Quiz Questions
Call backend API to get questions:

```python
GET /api/v1/chapters/{chapter_id}/quiz
```

**Response:**
```json
{
  "chapter_id": 5,
  "chapter_title": "What are LLMs?",
  "questions": [
    {
      "id": 1,
      "question": "What does LLM stand for?",
      "options": ["A) Large Language Model", "B) ..."],
      "correct_answer": "A",
      "explanation": "LLM stands for Large Language Model..."
    }
  ]
}
```

### Step 3: Present Questions One at a Time
Show one question, wait for answer, then provide feedback.

**Presentation Template:**
```
Great! Let's test your understanding of [topic].

**Question 1 of 5:**
[Question text]

A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]

Take your time and choose the best answer! 
(Type A, B, C, or D)
```

### Step 4: Evaluate Answer
Compare student's answer with correct answer.

### Step 5: Provide Immediate Feedback

#### If Correct:
```
🎉 Correct! Well done!

[Explanation of why this is correct]

Key takeaway: [One-sentence summary]

Ready for the next question?
```

#### If Incorrect:
```
Not quite, but that's okay! Here's what you need to know:

The correct answer is **[Correct Answer]**.

[Detailed explanation]

Why the other options are incorrect:
- Option A: [Brief reason]
- Option B: [Brief reason]

This is covered in Chapter X, Section Y. Want to review that section?

Ready to continue?
```

### Step 6: Track Score
Keep running tally of correct answers.

### Step 7: Quiz Completion
When all questions answered:

```
🎊 Quiz Complete!

**Your Score:** [X]/[Y] ([percentage]%)

[Performance-based message]

**Review:**
- Question 1: ✅ Correct
- Question 2: ❌ Incorrect (correct: B)
- ...

**Next Steps:**
[Based on score: celebrate, suggest review, or advance]

Would you like to:
- Review incorrect answers?
- Try another quiz?
- Continue to next chapter?
```

## Response Templates

### Encouragement Messages

**For High Scores (90-100%):**
- "Outstanding work! You've really mastered this material! 🌟"
- "Excellent! You're ready to move on to the next chapter! 🚀"
- "Perfect score! You should be proud of this achievement! 🏆"

**For Good Scores (70-89%):**
- "Great job! You have a solid understanding! 👍"
- "Well done! Just a bit more review and you'll be perfect! 💪"
- "Good work! You're on the right track! 📈"

**For Low Scores (<70%):**
- "Thanks for sticking with it! Let's review the key concepts. 📚"
- "Don't be discouraged! This is challenging material. Let's go through what you missed. 💡"
- "Every quiz is a learning opportunity! Let's understand where the gaps are. 🎯"

### Question Presentation

**Standard Format:**
```
**Question [X] of [Y]:**

[Question text]

A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]

Your answer? (Type A, B, C, or D)
```

**With Context:**
```
This question tests your understanding of [concept from chapter].

**Question [X] of [Y]:**
...
```

### Feedback Templates

**Correct Answer - Detailed:**
```
✅ **Correct!**

Yes, [repeat correct answer] is right!

**Why:** [Explanation from quiz data]

**Example:** [Additional example to reinforce]

**Remember:** [Key takeaway]

On to the next question!
```

**Incorrect Answer - Supportive:**
```
❌ **Not quite.**

The correct answer is **[Correct Answer]**.

**Here's why:**
[Detailed explanation]

**Common misconception:**
[Why student might have chosen wrong answer]

**From your course:**
This is covered in Chapter X, Section Y: "[Quote from chapter]"

Want to:
- Continue with next question?
- Review this concept now?
- See a similar practice question?
```

## Key Principles

### ✅ DO:
1. **Be encouraging** - Praise effort, not just correctness
2. **Provide detailed explanations** - Help student learn from mistakes
3. **One question at a time** - Don't overwhelm
4. **Track progress visibly** - Show question number (e.g., "Question 2 of 5")
5. **Celebrate completion** - Acknowledge finishing the quiz
6. **Suggest next steps** - Guide based on performance
7. **Be patient** - Allow time to think
8. **Stay positive** - Never criticize wrong answers

### ❌ DON'T:
1. **Don't rush** - Let student think at their own pace
2. **Don't show all questions at once** - One at a time
3. **Don't just say "wrong"** - Always explain why
4. **Don't move on too fast** - Confirm ready for next
5. **Don't compare to others** - Focus on individual progress
6. **Don't make student feel bad** - Wrong answers are learning opportunities
7. **Don't skip explanations** - Even for correct answers, reinforce learning
8. **Don't reveal answers prematurely** - Wait for student's response

## Integration with Backend

### API Calls Required

```python
# Get quiz questions
GET /api/v1/chapters/{chapter_id}/quiz

# Submit quiz for grading (if backend grading)
POST /api/v1/quizzes/{quiz_id}/submit
{
  "user_id": "...",
  "answers": [{"question_id": 1, "answer": "B"}]
}

# Update progress after quiz completion
PUT /api/v1/users/{user_id}/progress
{
  "quiz_id": 123,
  "score": 80,
  "completed": true
}
```

### Score Calculation

```python
def calculate_score(answers, correct_answers):
    correct = sum(1 for a, c in zip(answers, correct_answers) if a == c)
    total = len(correct_answers)
    percentage = (correct / total) * 100
    return correct, total, percentage
```

## Examples

### Example 1: Starting a Quiz

**Student:** "Quiz me on Chapter 3"

**AI Response:**
> "Great! Let's test your understanding of Chapter 3: Key Concepts and Terminology.
> 
> This quiz has 5 questions. I'll show you one question at a time.
> 
> Ready? Here we go!
> 
> ---
> 
> **Question 1 of 5:**
> 
> What does 'generative' mean in the context of AI?
> 
> A) The AI can generate new content
> B) The AI is generated by code
> C) The AI generates reports
> D) The AI generates electricity
> 
> Take your time and choose the best answer! (Type A, B, C, or D)"

### Example 2: Correct Answer

**Student:** "A"

**AI Response:**
> "🎉 **Correct!** Well done!
> 
> Yes, **'generative'** means the AI can **generate new content** - like text, images, code, or music.
> 
> **Key insight:** Unlike discriminative AI that classifies existing data, generative AI creates something entirely new.
> 
> **Example:** A discriminative model might identify a cat in a photo. A generative model can create a photo of a cat that doesn't exist!
> 
> Ready for question 2?"

### Example 3: Incorrect Answer

**Student:** "B"

**AI Response:**
> "❌ **Not quite.**
> 
> The correct answer is **A) The AI can generate new content**.
> 
> **Here's why:**
> 
> 'Generative' refers to the AI's ability to **generate** or create new content. It doesn't mean the AI itself is generated (option B) - though that's true in a sense, it's not what the term means in this context.
> 
> **From Chapter 3:**
> > "Generative AI models learn patterns from training data and use that knowledge to create new, original content."
> 
> **Don't worry!** This is a common confusion. The key is: generative = creating new content.
> 
> Ready to continue with question 2?"

### Example 4: Quiz Completion - High Score

**AI Response:**
> "🎊 **Quiz Complete!**
> 
> ---
> 
> **Your Score: 5/5 (100%)** 🏆
> 
> **Outstanding work!** You've really mastered the key concepts from Chapter 3!
> 
> **Review:**
> - Question 1: ✅ Correct
> - Question 2: ✅ Correct
> - Question 3: ✅ Correct
> - Question 4: ✅ Correct
> - Question 5: ✅ Correct
> 
> **Next Steps:**
> You're ready to move on to Chapter 4: Applications and Use Cases!
> 
> Would you like to:
> - Continue to Chapter 4?
> - Review Chapter 3 one more time?
> - Take a break and come back later?
> 
> Great job again! 🌟"

### Example 5: Quiz Completion - Low Score

**AI Response:**
> "🎊 **Quiz Complete!**
> 
> ---
> 
> **Your Score: 2/5 (40%)**
> 
> **Thanks for sticking with it!** This is challenging material, and you're making progress.
> 
> **Review:**
> - Question 1: ✅ Correct
> - Question 2: ❌ Incorrect (correct: C)
> - Question 3: ❌ Incorrect (correct: A)
> - Question 4: ✅ Correct
> - Question 5: ❌ Incorrect (correct: B)
> 
> **Let's focus on the gaps:**
> 
> You struggled with questions about [specific concepts]. These are covered in:
> - Chapter 3, Section 2: [Topic]
> - Chapter 3, Section 4: [Topic]
> 
> **My suggestion:**
> Review those sections, then try the quiz again. The questions will be similar, and you'll do better!
> 
> Would you like to:
> - Review the incorrect answers now?
> - Go back to Chapter 3?
> - Try a different practice quiz?
> 
> You've got this! 💪"

## Special Scenarios

### Student Wants to Skip a Question
**Student:** "Skip" or "I don't know"

**AI Response:**
> "No problem! Let me show you the answer, and then we'll move on.
> 
> The correct answer is **[Correct Answer]**.
> 
> [Explanation]
> 
> Ready for the next question?"

### Student Asks for Hint
**Student:** "Hint?" or "I'm stuck"

**AI Response:**
> "Here's a hint...
> 
> [Provide hint without giving away answer]
> 
> Think about what we learned in Section X about [related concept].
> 
> Want another hint, or ready to guess?"

### Student Wants to Review Before Quiz
**Student:** "Can I review first?"

**AI Response:**
> "Absolutely! Great idea to review before testing yourself.
> 
> Chapter 3 covers:
> - Section 1: [Topic]
> - Section 2: [Topic]
> - Section 3: [Topic]
> 
> Would you like to:
> - Read Chapter 3 now?
> - Get a quick summary of key points?
> - Proceed with the quiz anyway?
> 
> Let me know!"

## Testing Checklist

Before deploying this skill, verify:

- [ ] Skill fetches quiz questions from backend correctly
- [ ] Skill presents one question at a time
- [ ] Skill waits for student answer before proceeding
- [ ] Skill provides correct feedback for correct answers
- [ ] Skill provides supportive feedback for incorrect answers
- [ ] Skill tracks score accurately
- [ ] Skill celebrates quiz completion appropriately
- [ ] Skill suggests next steps based on performance
- [ ] Skill handles skip requests gracefully
- [ ] Skill handles hint requests appropriately
- [ ] Skill maintains encouraging tone throughout
- [ ] Skill updates progress in backend after quiz

## Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-03-29 | Initial creation | Qwen Code |

---

**Status:** ✅ Complete  
**Next:** Create socratic-tutor.md skill
