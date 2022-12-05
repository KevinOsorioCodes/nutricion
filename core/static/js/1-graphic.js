const ctx = document.getElementById('grafico-encuestas');
const de1 = document.getElementById('de1').textContent;
const de2 = document.getElementById('de2').textContent;
const de3 = document.getElementById('de3').textContent;



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