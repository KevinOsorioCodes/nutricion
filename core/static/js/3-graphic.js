const ctx = document.getElementById('grafico-encuestass');
const de1 = document.getElementById('des1').textContent;
const de2 = document.getElementById('des2').textContent;
const de3 = document.getElementById('des3').textContent;



const data = {
    labels: [
        'Excelente',
        'Regular',
        'Pesima'
    ],
    datasets: [{
        label: 'Encuestas',
        
        data: [de1, de2, de3],
        backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(54, 162, 235)',
            'rgb(255, 205, 86)'
        ],
        hoverOffset: 4,
    }]
};
const config = {
    type: 'doughnut',
    data: data,
};

new Chart(ctx, config);