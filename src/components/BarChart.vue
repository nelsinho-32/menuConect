<template>
  <Bar :data="chartData" :options="chartOptions" />
</template>

<script setup>
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

defineProps({
  chartData: {
    type: Object,
    required: true
  }
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false, // Esconde a legenda, pois o título do card já diz o que é
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      ticks: {
        // Formata o eixo Y para mostrar "R$"
        callback: function(value) {
          return 'R$ ' + value.toLocaleString('pt-BR');
        }
      }
    }
  }
};
</script>