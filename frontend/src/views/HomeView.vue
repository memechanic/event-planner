<template>
  <div class="home">
    <div class="hero">
      <h1>🗓️ Event Planner</h1>
      <p class="subtitle">Простое планирование встреч с друзьями и коллегами</p>
      
      <div class="cta-buttons">
        <router-link to="/create" class="primary-btn">
          📅 Создать событие
        </router-link>
        <router-link to="/event/demo" class="secondary-btn">
          🎯 Посмотреть демо
        </router-link>
      </div>
    </div>
    
    <div class="features">
      <div class="feature">
        <div class="feature-icon">📱</div>
        <h3>Просто и понятно</h3>
        <p>Создайте событие за минуту, отправьте ссылку участникам</p>
      </div>
      
      <div class="feature">
        <div class="feature-icon">🗳️</div>
        <h3>Голосование за даты</h3>
        <p>Участники выбирают удобное время, вы видите результаты</p>
      </div>
      
      <div class="feature">
        <div class="feature-icon">👥</div>
        <h3>Без регистрации</h3>
        <p>Никаких сложных форм, работает сразу по ссылке</p>
      </div>
    </div>
    
    <div class="how-it-works">
      <h2>Как это работает</h2>
      <ol>
        <li>Создайте событие с названием и вариантами дат</li>
        <li>Отправьте ссылку друзьям или коллегам</li>
        <li>Участники голосуют за удобные даты</li>
        <li>Вы видите результаты и выбираете лучшую дату</li>
      </ol>
    </div>
  </div>
</template>

<script setup>
// Главная страница не требует логики
</script>

<style scoped>
.home {
  max-width: 1000px;
  margin: 0 auto;
  padding: 40px 20px;
}

.hero {
  text-align: center;
  margin-bottom: 60px;
}

.hero h1 {
  font-size: 48px;
  margin-bottom: 10px;
  color: #333;
}

.subtitle {
  font-size: 18px;
  color: #666;
  margin-bottom: 30px;
}

.cta-buttons {
  display: flex;
  gap: 15px;
  justify-content: center;
  flex-wrap: wrap;
}

.primary-btn, .secondary-btn {
  padding: 14px 28px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  font-size: 16px;
  transition: all 0.3s;
}

.primary-btn {
  background: linear-gradient(135deg, #2196F3, #1976D2);
  color: white;
}

.primary-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(33, 150, 243, 0.3);
}

.secondary-btn {
  background: white;
  color: #2196F3;
  border: 2px solid #2196F3;
}

.secondary-btn:hover {
  background: #f0f7ff;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 30px;
  margin-bottom: 60px;
}

.feature {
  text-align: center;
  padding: 30px 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.feature-icon {
  font-size: 48px;
  margin-bottom: 20px;
}

.feature h3 {
  margin: 0 0 10px 0;
  color: #333;
}

.feature p {
  color: #666;
  line-height: 1.5;
}

.how-it-works {
  background: #f8f9fa;
  padding: 30px;
  border-radius: 12px;
}

.how-it-works h2 {
  margin-top: 0;
  color: #333;
}

.how-it-works ol {
  padding-left: 20px;
  font-size: 16px;
  line-height: 1.8;
}

.how-it-works li {
  margin-bottom: 10px;
  color: #555;
}

@media (max-width: 768px) {
  .hero h1 {
    font-size: 36px;
  }
  
  .cta-buttons {
    flex-direction: column;
    align-items: center;
  }
  
  .primary-btn, .secondary-btn {
    width: 100%;
    max-width: 300px;
    text-align: center;
  }
  
  .features {
    grid-template-columns: 1fr;
  }
}
</style>