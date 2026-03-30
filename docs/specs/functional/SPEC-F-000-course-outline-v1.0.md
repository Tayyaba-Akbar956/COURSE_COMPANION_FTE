# SPEC-F-000-course-outline-v1.0

## Status
- [x] Draft
- [ ] Pending Approval
- [ ] Approved
- [ ] In Progress
- [ ] Completed
- [ ] Deprecated

## Metadata
- **Created:** 2026-03-29
- **Author:** Qwen Code (AI Builder)
- **Approved By:** [Pending User Approval]
- **Version:** 1.0.0

## 1. Overview

This spec defines the complete course structure for "Generative AI Fundamentals" - a 24-chapter intermediate-level course covering LLMs, prompt engineering, RAG, fine-tuning, and practical applications.

## 2. Course Structure

### Course Metadata

| Attribute | Value |
|-----------|-------|
| **Course Title** | Generative AI Fundamentals |
| **Target Audience** | Intermediate learners (know basic Python) |
| **Total Chapters** | 24 chapters |
| **Total Modules** | 6 modules |
| **Estimated Duration** | 8-12 weeks (self-paced) |
| **Difficulty Level** | Intermediate |
| **Prerequisites** | Basic Python programming |
| **License** | Open Source |

### Module Breakdown

#### Module 1: Introduction to Generative AI (Chapters 1-4)
- **Chapter 1:** What is Generative AI?
- **Chapter 2:** Evolution of AI: From Discriminative to Generative
- **Chapter 3:** Key Concepts and Terminology
- **Chapter 4:** Applications and Use Cases

#### Module 2: Understanding Large Language Models (Chapters 5-8)
- **Chapter 5:** What are LLMs?
- **Chapter 6:** How LLMs Work: Transformers Architecture
- **Chapter 7:** Training and Pre-training LLMs
- **Chapter 8:** LLM Capabilities and Limitations

#### Module 3: Prompt Engineering Fundamentals (Chapters 9-12)
- **Chapter 9:** Introduction to Prompt Engineering
- **Chapter 10:** Prompt Design Patterns and Techniques
- **Chapter 11:** Advanced Prompting Strategies
- **Chapter 12:** Prompt Optimization and Best Practices

#### Module 4: Retrieval Augmented Generation (RAG) (Chapters 13-16)
- **Chapter 13:** What is RAG and Why It Matters
- **Chapter 14:** Building a RAG System
- **Chapter 15:** Vector Databases and Embeddings
- **Chapter 16:** RAG Best Practices and Optimization

#### Module 5: Fine-tuning and Customization (Chapters 17-20)
- **Chapter 17:** Introduction to Fine-tuning
- **Chapter 18:** When to Fine-tune vs. Prompt Engineering
- **Chapter 19:** Fine-tuning Methods and Techniques
- **Chapter 20:** Evaluating Fine-tuned Models

#### Module 6: Building Generative AI Applications (Chapters 21-24)
- **Chapter 21:** Designing AI-Native Applications
- **Chapter 22:** Building with APIs (OpenAI, Anthropic, etc.)
- **Chapter 23:** Deployment and Production Considerations
- **Chapter 24:** Ethics, Safety, and Responsible AI

## 3. Chapter Content Template

Each chapter will follow this structure:

```markdown
# Chapter X: [Chapter Title]

## Learning Objectives
- Objective 1
- Objective 2
- Objective 3

## Introduction
[Brief introduction to the topic]

## Core Concepts
[Detailed explanation of concepts]

### Code Example
```python
# Relevant code example
```

## Key Takeaways
- Point 1
- Point 2
- Point 3

## Glossary
- **Term 1:** Definition
- **Term 2:** Definition

## Quiz Questions
1. Question?
   - A) Option A
   - B) Option B
   - C) Option C
   - D) Option D
   - **Correct Answer:** B
   - **Explanation:** Why B is correct

2. Question?
   [Same format]

## Further Reading
- [Resource links]
```

## 4. Freemium Gate

| Tier | Access |
|------|--------|
| **Free Users** | Module 1 (Chapters 1-4) |
| **Premium Users** | All 24 chapters |

**Note:** Adjusted from original 3 chapters to 4 chapters (entire Module 1) for better learning experience.

## 5. Learning Outcomes

After completing this course, students will be able to:

1. **Understand** the fundamentals of generative AI and LLMs
2. **Apply** prompt engineering techniques effectively
3. **Build** RAG systems for domain-specific applications
4. **Evaluate** when to use fine-tuning vs. prompting
5. **Design** and deploy generative AI applications
6. **Implement** responsible AI practices

## 6. Assessment Strategy

### Chapter Quizzes
- 5-10 multiple-choice questions per chapter
- Immediate feedback with explanations
- Minimum 80% to pass

### Module Assessments (Phase 2 Feature)
- Comprehensive quizzes at end of each module
- LLM-graded open-ended questions
- Practical coding exercises

### Final Project (Phase 3 Feature)
- Build a complete generative AI application
- Peer review and evaluation
- Certificate of completion

## 7. Dependencies

This spec depends on:
- SPEC-T-001-database-schema-v1.0.md (for storing chapter data)
- SPEC-A-001-content-apis-v1.0.md (for serving content)

## 8. Out of Scope

This spec does NOT cover:
- Detailed chapter content (will be created separately)
- Video content (text-only course)
- Live tutoring sessions (asynchronous learning)
- Certification accreditation

## 9. Testing Requirements

### Test Scenarios
1. Verify all 24 chapters are accessible via API
2. Verify module grouping is correct
3. Verify free users can access Module 1 only
4. Verify premium users can access all chapters
5. Verify chapter navigation (next/previous) works correctly

### Coverage Requirements
- 90% code coverage required
- All API endpoints tested
- Access control tested

## 10. Open Questions

1. Should we include hands-on coding exercises in each chapter?
2. Should we add difficulty ratings per chapter?
3. Should we include estimated time per chapter?

## 11. Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-03-29 | Initial draft | Qwen Code |

---

## 📋 APPROVAL REQUEST

**What:** Course Outline Spec (SPEC-F-000-course-outline-v1.0)  
**Why:** Defines the complete structure for our Generative AI Fundamentals course (24 chapters, 6 modules)  
**Files Affected:** 
- `docs/specs/functional/SPEC-F-000-course-outline-v1.0.md`

**Key Decisions:**
- 24 chapters total (can adjust to 20-30 as per hackathon requirements)
- 6 modules for logical grouping
- Module 1 (Chapters 1-4) free for better learning experience
- Intermediate level, requires basic Python

**Do you approve this course outline?** (Yes/No/Modify)
