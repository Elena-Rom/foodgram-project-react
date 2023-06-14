from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True,
        blank=False,
        null=False,
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=254,
        unique=True,
        blank=False,
        null=False,
    )

    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=True,
        null=False,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=True,
        null=False
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=150,
        blank=False,
        null=False,
    )
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name='Пользователь',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique follow',
            )
        ]

    def __str__(self):
        return f'{self.user} подписан на {self.author}'


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        unique=True,
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=7,
        unique=True,
        db_index=False,
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=200,
        unique=True,
        db_index=False,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name="Название ингредиента",
        max_length=200,
    )
    unit = models.CharField(
        verbose_name="Единица измерения",
        max_length=200,
    )

    class Meta:
        verbose_name = "Ингредиенты"

    def __str__(self):
        return f"{self.name}, {self.unit}"


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='recipes/',
        blank=True,
    )
    text = models.TextField(
        verbose_name='Описание',

    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации рецепта',
        auto_now_add=True,
        db_index=True
    )
    ingredients = models.ManyToManyField(
        Ingredient,

        verbose_name='Ингредиенты',
        blank=True,
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=[MinValueValidator(
            1,
            'Минимальное время для приготовления 1 минута')],
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipeingredients',
        verbose_name='Рецепт'

    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipeingredients',
        verbose_name='Ингредиент'
    )
    amount = models.PositiveIntegerField(
        null=True,
        verbose_name="Количество",
        validators=[MinValueValidator(
            1,
            'Минимальное количество ингридиентов 1')],
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name="favorite",
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="favorite",
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Избранное'
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique favorite recipe for user')
        ]

    def __str__(self):
        return f"{self.user} добавил {self.recipe} в избранное"


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='lists',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='lists',
        verbose_name='Рецепт'
    )
    date_add = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
        editable=False,
    )

    class Meta:
        ordering = ['-id']
        verbose_name = "Список покупок"
        verbose_name_plural = verbose_name
        constraints = [models.UniqueConstraint(
            fields=['user',
                    'recipe'],
            name='unique_numbers')]

    def __str__(self):
        return (f'{self.user} добавил'
                f'{self.recipe} в список покупок')
