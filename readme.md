# 🎬 Movie Recommendation System (Hybrid Approach)

## 📌 Project Overview
This project is a **Movie Recommendation System** developed using a **Hybrid Approach**.  
The system combines **user-based filtering, content-based filtering, and hybrid recommendation techniques** to deliver more personalized suggestions.

At the start, the system presents a **toggle box** asking for a **User ID**:
- 🔹 If the user is **new**, the system prompts them to **create a new User ID**.  
- 🔹 If the user is **existing**, the system recognizes them and provides tailored recommendations.  

This approach ensures that **new users** can easily get started, while **existing users** enjoy improved recommendations over time.

---

## ⚙️ Features
- ✅ **User-Friendly Toggle System**: Allows new and existing users to log in seamlessly.  
- ✅ **Hybrid Recommendation Engine**: Combines multiple approaches (Collaborative + Content-based).  
- ✅ **Personalization**: Recommendations improve as the user interacts more with the system.  
- ✅ **Scalable Design**: Can handle multiple users and large movie datasets.  

---

## 🧠 How the Hybrid Approach Works
1. **User Identification**  
   - New users → System assigns them an ID.  
   - Existing users → System fetches their profile.  

2. **Recommendation Generation**  
   - **Content-Based Filtering** → Suggests movies similar to ones the user liked.  
   - **Collaborative Filtering** → Uses ratings and preferences of similar users.  
   - **Hybrid Model** → Merges both approaches for better accuracy.  

3. **Final Output**  
   - Personalized movie recommendations are displayed to the user.  

---

## 🖥️ Tech Stack
- **Programming Language**: Python  
- **Libraries**: Pandas, NumPy, Scikit-learn, Surprise / LightFM (for hybrid filtering), Streamlit/Flask (UI)  
- **Database**: CSV's [ movies.csv, ratings.csv] / SQL for storing users and ratings  
- **Visualization**: Matplotlib / Seaborn (optional)  

---

## 🚀 How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/Priyanka17809211/MOvies-Recommender.git
   cd MOvies-Recommender
