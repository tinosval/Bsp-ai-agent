# 📋 BSP AI Agent

An AI-powered Behaviour Support Plan (BSP) generator built for NDIS providers using LangChain, OpenAI GPT, and Streamlit.

---

## 🚀 What It Does

- ✅ Staff enter client details via simple web form
- ✅ AI searches ONLY internal resource documents
- ✅ Generates professional BSP paragraphs automatically
- ✅ Flags any diagnosis not found in internal documents
- ✅ Downloads completed BSP as Word document instantly
- ✅ Supports both Interim and Comprehensive BSP plans

---

## 💡 The Problem It Solves

Writing Behaviour Support Plans manually takes experienced practitioners 4-8 hours per plan.

This AI agent reduces that to under 2 minutes while ensuring consistency and using only approved internal resources.

**Time saved: 96% reduction in BSP creation time**

---

## 🔧 Technologies Used

| Technology | Purpose |
|-----------|---------|
| Python | Core programming language |
| Streamlit | Web interface for staff |
| LangChain | AI agent framework |
| ChromaDB | Vector database for document search |
| OpenAI GPT-3.5/4 | AI content generation |
| python-docx | Word document generation |
| RAG System | Internal document search only |

---

## 📋 How It Works
1. **Enter client details** — Staff fill in a simple web form with client name, diagnosis, and behaviours of concern.
2. **AI searches internal documents** — The agent searches only the internal 60-page resource document using a RAG (Retrieval-Augmented Generation) system, never external sources.
3. **Flags missing information** — If a diagnosis or condition isn't found internally, the agent flags it instead of guessing or pulling from outside sources.
4. **Generates the plan** — The AI writes professional BSP paragraphs matching the tone and structure of existing plans.
5. **Download as Word** — The completed Behaviour Support Plan is generated and downloaded instantly as a formatted .docx file, ready for review.