const ctx = document.getElementById('grafico-fichas');
const df1 = document.getElementById('df1').textContent;
const df2 = document.getElementById('df2').textContent;




const data = {
    labels: [
        'Fichas del dia',
        'Fichas restantes'
    ],
    datasets: [{
        label: 'Fichas',
        
        data: [df2, df1-df2],
        backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(54, 162, 235)'
        ],
        hoverOffset: 4,
    }]
};
const config = {
    type: 'doughnut',
    data: data,
};

new Chart(ctx, config);