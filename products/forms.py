from django import forms
from .models import Product

class RegisterProductForm(forms.ModelForm):
    """
    Formulário para criação de produtos(cultivos).
    """

    class Meta:
        model = Product
        fields = (
            'nome',
            'especie',
        )

    def clean(self):
        """
        Validacao adicional para campos especificos.
        """
        cleaned_data = super().clean()
        # Exemplo de uma validação personalizada
        nome = cleaned_data.get('nome')
        especie = cleaned_data.get('especie')

        # Exemplo de validação: verificar se o nome não está vazio e a espécie não é igual ao nome
        if nome and especie and nome == especie:
            raise forms.ValidationError("O nome e a espécie não podem ser iguais.")
        
        return cleaned_data
