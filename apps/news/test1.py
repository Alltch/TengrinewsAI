from datetime import datetime
base_date = datetime.now().replace(day=datetime.now().day - 1)

clean_time_str = 'Сегодня | 12:59'
    
clean_time_str = clean_time_str.replace("Сегодня | ", "").strip()

time_part = datetime.strptime(clean_time_str, '%H:%M').time()


print(time_part)