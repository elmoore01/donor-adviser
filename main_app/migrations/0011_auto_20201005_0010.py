# Generated by Django 3.0.8 on 2020-10-05 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_auto_20201004_2307'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='contact_title',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='organization',
            name='category',
            field=models.CharField(choices=[('AG', 'Aging'), ('AF', 'Agriculture and Food'), ('AC', 'Arts and Culture'), ('AS', 'Athletics and Sports'), ('CY', 'Children and Youth'), ('AF', 'After School'), ('CS', 'Civil Society'), ('CE', 'Community and Economic Development'), ('CT', 'Computers and Technology'), ('CP', 'Consumer Protection'), ('CR', 'Crime and Safety'), ('DI', 'Disabilities'), ('DO', 'Domestic Violence Prevention'), ('EL', 'Education and Literacy'), ('K2', 'K 12'), ('HE', 'Higher Education'), ('CR', 'Career Preparation'), ('AE', 'Adult Education'), ('EM', 'Employment and Labor'), ('EE', 'Energy and Environment'), ('LI', 'LGBTQ+'), ('GR', 'Government Reform'), ('HW', 'Health and Wellness'), ('HO', 'Housing and Homelessness'), ('HR', 'Human Rights and Civil Liberties'), ('HU', 'Hunger'), ('IM', 'Immigration'), ('JM', 'Journalism and Media'), ('MB', 'Men and Boys'), ('NP', 'Nonprofit Empowerment'), ('PF', 'Parenting and Families'), ('PO', 'Poverty'), ('PJ', 'Prison and Judicial Reform'), ('RE', 'Race and Ethnicity'), ('RI', 'Religion'), ('SC', 'Science, Technology, Engineering and Math'), ('SA', 'Substance Abuse and Recovery'), ('TR', 'Transportation'), ('WE', 'Welfare and Public Assistance'), ('WG', 'Woman and Girls')], max_length=2),
        ),
    ]
