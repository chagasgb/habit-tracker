# 🧪 Testes - Habit Tracker API

Este diretório contém todos os testes automatizados para a API de rastreamento de hábitos.

## 📊 Cobertura de Testes

### 🎯 Testes de Habits (4 testes)
✅ **test_create_habit** - Criação de hábito básica  
✅ **test_get_all_habits** - Listagem de todos os hábitos  
✅ **test_delete_habit** - Exclusão de hábito  
✅ **test_delete_habit_not_found** - Exclusão de hábito inexistente  

### 🧹 Testes de Records (7 testes)
✅ **test_create_record** - Criação básica de registro  
✅ **test_get_all_records** - Listagem geral de registros  
✅ **test_get_records_by_habit** - Filtro por hábito  
✅ **test_create_record_invalid_habit** - Validação de hábito  
✅ **test_create_record_invalid_data** - Validação de dados  
✅ **test_delete_record** - Exclusão de registro  
✅ **test_delete_record_not_found** - Exclusão inexistente  

## 🚀 Como Executar

```bash
# Executar todos os testes
python -m pytest tests/ -v

# Executar apenas testes de habits
python -m pytest tests/test_habits.py -v

# Executar apenas testes de records
python -m pytest tests/test_records.py -v

# Executar com mais detalhes
python -m pytest tests/ -v -s
```

## 🎯 Total: 11 testes passando
