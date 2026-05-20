// Filtragem de seleções por grupo
document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('.filter-btn');
    const cards   = document.querySelectorAll('.selecao-card');
    const empty   = document.getElementById('empty-state');

    buttons.forEach(btn => {
        btn.addEventListener('click', () => {
            const grupo = btn.dataset.grupo;

            // Atualiza botão ativo
            buttons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            // Filtra cards
            let visiveis = 0;
            cards.forEach(card => {
                const match = grupo === 'todos' || card.dataset.grupo === grupo;
                card.style.display = match ? '' : 'none';
                if (match) visiveis++;
            });

            // Exibe mensagem de vazio se nenhum resultado
            if (empty) empty.style.display = visiveis === 0 ? '' : 'none';
        });
    });
});
