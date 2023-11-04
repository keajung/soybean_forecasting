
from flask import Flask,request,jsonify
from keras.preprocessing.sequence import TimeseriesGenerator
# from sklearn.preprocessing import MinMaxScaler

app = Flask(__name__)

@app.route('/predict_model',methods=['GET'])
def predict_model():
	from datetime import datetime
	import pandas as pd
	import tensorflow as tf

	# ----- รับข้อมูลจากหน้า web ---------
	d = {}
	d['Thai_Import'] = float(request.args['Thai_Import'])
	d['Soybean_meal_US'] = float(request.args['Soybean_meal_US'])
	d['Crude_Oil'] = float(request.args['Crude_Oil'])
	d['New_Month'] = float(request.args['New_Month'])
	d['Year'] = float(request.args['Year'])

	df_input = pd.DataFrame([d])  # แปลงเป็น dataframe
	# print(df_input.dtypes)
	# d['Soybean_meal_US'] = d['Soybean_meal_US'].astype(float)
	year = int(d['Year'])
	month = int(d['New_Month'])
	day = 1
	print('year')
	print(year - 543)

	if month == 1:
		start_date = datetime(year - 544, 10, day)  # 12 11 10
		end_date = datetime(year - 543, month, day)
	elif month == 2:
		start_date = datetime(year - 544, 11, day)  # 1 12 11
		end_date = datetime(year - 543, month, day)
	elif month == 3:
		start_date = datetime(year - 544, 12, day)  # 2 1 12
		end_date = datetime(year - 543, month, day)
	else:
		start_date = datetime(year - 543, month - 3, day)
		end_date = datetime(year - 543, month, day)
	#
	print('thai')
	print(d['Thai_Import'])
	print(end_date)
	print(start_date)

	# ------- อ่านข้อมูล excel  ---------

	df_crude_oil_data = pd.read_excel('crude_oil_data.xls')  # soybean_meal_data.xls
	df_soybean_meal_data = pd.read_excel('soybean_meal_data.xls')  # soybean_meal_data.xls
	# df_thai_import = pd.read_excel('dataofPrice_moveThaiPriceForOneStep.xlsx')  # soybean_meal_data.xls
	# ------- ทำ excel to array --------
	array_crude_oil_data = df_crude_oil_data.to_numpy()
	array_soybean_meal_data = df_soybean_meal_data.to_numpy()
	# array_thai_import_data = df_thai_import.to_numpy()
	# -------- ดึงข้อมูลที่ต้องการจาก array ไปใส่อีก array ----------
	new_crude_oil = []
	for i in range(len(array_crude_oil_data)):
		new_crude_oil.append([])
		for j in range(1, 3):
			if array_crude_oil_data[i][1] >= start_date and array_crude_oil_data[i][1] < end_date:
				new_crude_oil[i].append(array_crude_oil_data[i][j])
				print(array_crude_oil_data[i][j])

	new_soybean_meal = []
	for i in range(len(array_soybean_meal_data)):
		new_soybean_meal.append([])
		for j in range(1, 3):
			if array_soybean_meal_data[i][1] >= start_date and array_soybean_meal_data[i][1] < end_date:
				new_soybean_meal[i].append(array_soybean_meal_data[i][j])
				print(array_soybean_meal_data[i][j])

	# new_thai_import = []
	# for i in range(len(array_thai_import_data)):
	# 	new_thai_import.append([])
	# 	for j in range(0, 2):
	# 		if array_thai_import_data[i][0] >= start_date and array_thai_import_data[i][0] < end_date:
	# 			new_thai_import[i].append(array_thai_import_data[i][j])
	# #             print(new_thai_import[i][j])

	# ทำ new array to dataframe and drop all Nan or NaT
	soybean_meal_complete = pd.DataFrame(new_soybean_meal, columns=['Date', 'Soybean_meal_us'])
	soybean_meal_complete = soybean_meal_complete.dropna()
	crude_oil_complete = pd.DataFrame(new_crude_oil, columns=['Date', 'Crude_Oil'])
	crude_oil_complete = crude_oil_complete.dropna()
	# thai_import_complete = pd.DataFrame(new_thai_import, columns=['Date', 'Thai_Import'])
	# thai_import_complete = thai_import_complete.dropna()
	print('♥♥soybean_meal_complete')
	print(soybean_meal_complete)
	print('♥♥crude_oil_complete')
	print(crude_oil_complete)
	print('♥♥thai_import_complete')

	# แยก เดือน ปี
	soybean_meal_complete['New_Month'] = pd.to_datetime(soybean_meal_complete['Date']).dt.strftime('%m').astype('int')
	soybean_meal_complete['Year'] = pd.to_datetime(soybean_meal_complete['Date']).dt.strftime('%Y').astype('int')
	crude_oil_complete['New_Month'] = pd.to_datetime(crude_oil_complete['Date']).dt.strftime('%m').astype('int')
	crude_oil_complete['Year'] = pd.to_datetime(crude_oil_complete['Date']).dt.strftime('%Y').astype('int')
	# thai_import_complete['New_Month'] = pd.to_datetime(thai_import_complete['Date']).dt.strftime('%m').astype('int')
	# thai_import_complete['Year'] = pd.to_datetime(thai_import_complete['Date']).dt.strftime('%Y').astype('int')

	soybean_meal_complete = soybean_meal_complete[['New_Month', 'Year', 'Soybean_meal_us']]
	crude_oil_complete = crude_oil_complete[['New_Month', 'Year', 'Crude_Oil']]
	# thai_import_complete = thai_import_complete[['New_Month', 'Year', 'Thai_Import']]

	print('newwwwwwwwwwwwwwwwwwwww♥♥♥')
	# print(crude_oil_complete)
	print(soybean_meal_complete)

	# --------- ทำ array check status เดือนที่ขาดของ crude oil and soybean และ thai_import----------
	import numpy as np

	# array status
	check = []
	reverse = 12
	print('startttttttttttttttttttttt')
	print(month)

	for i in range(4):
		if (month <= 0):
			check.append((reverse, 0))
			reverse = reverse - 1
		else:
			check.append((month, 0))
		month = month - 1
		crude_oil_mat_vals = np.vstack(check)
		soybean_mat_vals = np.vstack(check)
		thai_import_vals = np.vstack(check)

	print('check stata')
	print(check)
	# new array
	crude_oil_mat_vals = np.delete(crude_oil_mat_vals, 0, 0)
	soybean_mat_vals = np.delete(soybean_mat_vals, 0, 0)
	thai_import_vals = np.delete(thai_import_vals, 0, 0)

	# --------- check shape dataframe ของ Crud oil and Soybean meal ถ้าไม่ครบก็จะไปใส่สถานะ ใน array soybean_mat_vals / crude_oil_mat_vals
	# ของ THAI IMPORT
	# if thai_import_complete.shape == (3, 2):
	# 	print('yes')
	# else:
	# 	# ใส่สถานะว่าเดือนไหนมีข้อมูล
	# 	array_thai_import_for_status = np.array(thai_import_complete)
	# 	for i in range(len(thai_import_vals)):
	# 		for j in range(len(array_thai_import_for_status)):
	# 			if thai_import_vals[i][0] == int(array_thai_import_for_status[j][0]):
	# 				print(thai_import_vals[i][0])
	# 				thai_import_vals[i][1] = 1
	# print('----------thai_import_vals-----------')
	# print(thai_import_vals)

	# ของ SOYBEAN MEAL
	if soybean_meal_complete.shape == (3, 2):
		print('yes')
	else:
		# ใส่สถานะว่าเดือนไหนมีข้อมูล
		array_soybean_for_status = np.array(soybean_meal_complete)
		for i in range(len(soybean_mat_vals)):
			for j in range(len(array_soybean_for_status)):
				if soybean_mat_vals[i][0] == int(array_soybean_for_status[j][0]):
					print(soybean_mat_vals[i][0])
					soybean_mat_vals[i][1] = 1
	print('----------soybean_mat_vals-----------')
	print(soybean_mat_vals)

	# ของ CRUDE OIL
	if crude_oil_complete.shape == (3, 2):
		print('yes')
	else:
		# ใส่สถานะว่าเดือนไหนมีข้อมูล
		array_crude_oil_for_status = np.array(crude_oil_complete)
		for i in range(len(crude_oil_mat_vals)):
			for j in range(len(array_crude_oil_for_status)):
				if crude_oil_mat_vals[i][0] == int(array_crude_oil_for_status[j][0]):
					print(crude_oil_mat_vals[i][0])
					crude_oil_mat_vals[i][1] = 1

	print('----------crude_oil_mat_vals-----------')
	print(crude_oil_mat_vals)

	# ปริ้นอาเรย์เช็คสถานะออกมาดู count เอาไว้นับจำนวนเดือนที่ขาดเพื่อใช้ใน loop ถัดไป
	# count_null_thai_import = 0
	# for i in range(len(thai_import_vals)):
	# 	for j in range(2):
	# 		if thai_import_vals[i][j] == 0:
	# 			count_null_thai_import += 1
	# print('count_null_thai_import')
	# print(count_null_thai_import)
	# #
	count_null_soybean = 0
	for i in range(len(soybean_mat_vals)):
		for j in range(2):
			if soybean_mat_vals[i][j] == 0:
				count_null_soybean += 1
	print('count_null_soybean')
	print(count_null_soybean)
	#
	count_null_crude_oil = 0
	for i in range(len(crude_oil_mat_vals)):
		for j in range(2):
			if crude_oil_mat_vals[i][j] == 0:
				count_null_crude_oil += 1
	print('count_null_crude_oil')
	print(count_null_crude_oil)

	# ใส่ null to ะ้ฟร๘รทยนพะ / crude oil dataframe  / and soybean meal สำหรับเดือนที่ขาด

	# # thai_import
	# for i in range(len(thai_import_vals)):
	# 	if thai_import_vals[i][1] == 0:
	# 		if thai_import_vals[i][0] == 12:
	#
	# 			fill_Null_thai = {'New_Month': thai_import_vals[i][0], 'Year': year - 544, 'Thai_Import': [np.nan]}
	# 			fill_Null_Data_thai = pd.DataFrame(fill_Null_thai)  # แปลงเป้น dataframe
	# 			# รวม dataframe ข้อมูลที่มีกับข้อมูลที่ null เข้าด้วยกันแล้ว sort และเติมค่า mean
	# 			# print('result_for_predict----')
	# 			# print(result_for_predict)
	# 			# print('------------')
	# 			frames_thai = [thai_import_complete, fill_Null_Data_thai]
	#
	# 			# print('frames1')
	# 			# print(frames1)
	# 			# print('----')
	# 			thai_import_complete = pd.concat(frames_thai)
	#
	# 			# print('result_for_predict1')
	# 			# print(result_for_predict)
	# 			# print('-------------')
	# 			thai_import_complete = thai_import_complete.sort_values(by=['New_Month'])
	# 			thai_import_complete = thai_import_complete.fillna(thai_import_complete.mean())
	# 		#
	# 		# print(fill_Null_Data)
	# 		# print(result_for_predict)
	# 		# print('----------------')
	# 		#
	# 		else:
	# 			fill_Null_thai = {'New_Month': thai_import_vals[i][0], 'Year': year - 543, 'Thai_Import': [np.nan]}
	# 			fill_Null_Data_thai = pd.DataFrame(fill_Null_thai)  # แปลงเป้น dataframe
	# 			# รวม dataframe ข้อมูลที่มีกับข้อมูลที่ null เข้าด้วยกันแล้ว sort และเติมค่า mean
	# 			# print('result_for_predict----')
	# 			# print(result_for_predict)
	# 			# print('------------')
	# 			frames_thai = [thai_import_complete, fill_Null_Data_thai]
	#
	# 			# print('frames1')
	# 			# print(frames1)
	# 			# print('----')
	# 			thai_import_complete = pd.concat(frames_thai)
	#
	# 			# print('result_for_predict1')
	# 			# print(result_for_predict)
	# 			# print('-------------')
	# 			thai_import_complete = thai_import_complete.sort_values(by=['New_Month'])
	# 			thai_import_complete = thai_import_complete.fillna(thai_import_complete.mean())
	#
	# 	print('fill_Null_Data')
	# 	print('thai_import_complete')
	# 	# print(fill_Null_Data_soy)
	# 	print(thai_import_complete)
	# 	print('----------------')

	# soybean
	for i in range(len(soybean_mat_vals)):
		if soybean_mat_vals[i][1] == 0:
			if soybean_mat_vals[i][0] == 12:

				fill_Null_Soy = {'New_Month': soybean_mat_vals[i][0], 'Year': year - 544, 'Soybean_meal_us': [np.nan]}
				fill_Null_Data_soy = pd.DataFrame(fill_Null_Soy)  # แปลงเป้น dataframe
				# รวม dataframe ข้อมูลที่มีกับข้อมูลที่ null เข้าด้วยกันแล้ว sort และเติมค่า mean
				# print('result_for_predict----')
				# print(result_for_predict)
				# print('------------')
				frames_soy = [soybean_meal_complete, fill_Null_Data_soy]

				# print('frames1')
				# print(frames1)
				# print('----')
				soybean_meal_complete = pd.concat(frames_soy)

				# print('result_for_predict1')
				# print(result_for_predict)
				# print('-------------')
				soybean_meal_complete = soybean_meal_complete.sort_values(by=['New_Month'])
				soybean_meal_complete = soybean_meal_complete.fillna(soybean_meal_complete.mean())
			#
			# print(fill_Null_Data)
			# print(result_for_predict)
			# print('----------------')
			#
			else:
				fill_Null_soy = {'New_Month': soybean_mat_vals[i][0], 'Year': year - 543, 'Soybean_meal_us': [np.nan]}
				fill_Null_Data_soy = pd.DataFrame(fill_Null_soy)  # แปลงเป้น dataframe
				# รวม dataframe ข้อมูลที่มีกับข้อมูลที่ null เข้าด้วยกันแล้ว sort และเติมค่า mean
				# print('result_for_predict----')
				# print(result_for_predict)
				# print('------------')
				frames_soy = [soybean_meal_complete, fill_Null_Data_soy]

				# print('frames1')
				# print(frames1)
				# print('----')
				soybean_meal_complete = pd.concat(frames_soy)

				# print('result_for_predict1')
				# print(result_for_predict)
				# print('-------------')
				soybean_meal_complete = soybean_meal_complete.sort_values(by=['New_Month'])
				soybean_meal_complete = soybean_meal_complete.fillna(soybean_meal_complete.mean())

		print('fill_Null_Data_soy')
		print('soybean_meal_complete')
		# print(fill_Null_Data_soy)
		print(soybean_meal_complete)
		print('----------------')

	# crude oil

	for i in range(len(crude_oil_mat_vals)):
		if crude_oil_mat_vals[i][1] == 0:
			if crude_oil_mat_vals[i][0] == 12:

				fill_Null_oil = {'New_Month': crude_oil_mat_vals[i][0], 'Year': year - 544, 'Crude_Oil': [np.nan]}
				fill_Null_oil = pd.DataFrame(fill_Null_oil)  # แปลงเป้น dataframe
				# รวม dataframe ข้อมูลที่มีกับข้อมูลที่ null เข้าด้วยกันแล้ว sort และเติมค่า mean
				# print('result_for_predict----')
				# print(result_for_predict)
				# print('------------')
				frames_oil = [crude_oil_complete, fill_Null_oil]

				# print('frames1')
				# print(frames1)
				# print('----')
				crude_oil_complete = pd.concat(frames_oil)

				# print('result_for_predict1')
				# print(result_for_predict)
				# print('-------------')
				crude_oil_complete = crude_oil_complete.sort_values(by=['New_Month'])
				crude_oil_complete = crude_oil_complete.fillna(crude_oil_complete.mean())
			#
			# print(fill_Null_Data)
			# print(result_for_predict)
			# print('----------------')
			#
			else:
				fill_Null_oil = {'New_Month': crude_oil_mat_vals[i][0], 'Year': year - 543, 'Crude_Oil': [np.nan]}
				fill_Null_Data_oil = pd.DataFrame(fill_Null_oil)  # แปลงเป้น dataframe
				# รวม dataframe ข้อมูลที่มีกับข้อมูลที่ null เข้าด้วยกันแล้ว sort และเติมค่า mean
				# print('result_for_predict----')
				# print(result_for_predict)
				# print('------------')
				frames_oil = [crude_oil_complete, fill_Null_Data_oil]

				# print('frames1')
				# print(frames1)
				# print('----')
				crude_oil_complete = pd.concat(frames_oil)

				# print('result_for_predict1')
				# print(result_for_predict)
				# print('-------------')
				crude_oil_complete = crude_oil_complete.sort_values(by=['New_Month'])
				crude_oil_complete = crude_oil_complete.fillna(crude_oil_complete.mean())

		print('fill_Null_Data_oil')
		print('crude_oil_complete')
		print(crude_oil_complete)
	# print(fill_Null_Data_oil)

	# เอา dataframe 3  อันมารวมกัน crude_oil_complete+soybean_meal_complete+thai_import
	new_soybean_for_concat = pd.DataFrame(soybean_meal_complete, columns=['Soybean_meal_us'])
	new_oil_for_concat = pd.DataFrame(crude_oil_complete, columns=['Crude_Oil'])
	# new_thai_for_concat = pd.DataFrame(0, columns=['Thai_Import'])

	new_soybean_for_concat = new_soybean_for_concat.reset_index(drop=True)
	new_oil_for_concat = new_oil_for_concat.reset_index(drop=True)
	# new_thai_for_concat = new_thai_for_concat.reset_index(drop=True)


	data_from_excel_complete = pd.concat([new_oil_for_concat, new_soybean_for_concat], axis=1)

	print('เอา dataframe 3 อันมารวมกัน crude_oil_complete+soybean_meal_complete')
	print(data_from_excel_complete)
	# ----------------------------------จัดการ data excel เสร็จแล้ว -------------------------------------------.

	# ข้อมูล Input user from User Interface
	user_input = [[d['Thai_Import'], d['Crude_Oil'], d['Soybean_meal_US']]]
	print('#ข้อมูล Input user from User Interface')
	print(user_input)
	# เอา dataframe data_from_excel_complete มารวม ข้อมูลจากผู้ใช้ที่หน้า UI
	user_input_for_concat = pd.DataFrame(user_input, columns=['Thai_Import', 'Crude_Oil', 'Soybean_meal_us'])
	user_input_for_concat = user_input_for_concat.reset_index(drop=True)
	data_from_excel_complete = data_from_excel_complete.reset_index(drop=True)
	frames_last = [data_from_excel_complete, user_input_for_concat]
	complete_all_data = pd.concat(frames_last)

	print('-----------------------complete_all_data-----------------------')
	print(complete_all_data)
	complete_all_data = complete_all_data.fillna(d['Thai_Import'])

	new_column = ['Thai_Import', 'Crude_Oil', 'Soybean_meal_us']
	complete_all_data = complete_all_data[new_column]
	complete_all_data = complete_all_data.reindex(columns=new_column)
	# ----------------------------------จัดการ data ทุกอย่างเรียบร้อย -------------------------------------------.

	# # dataframe reslut for predict1 to array for predict
	list_for_predict = complete_all_data.values.tolist()
	list_for_predict
	array_for_predict = np.array(list_for_predict)
	print(array_for_predict.shape)  # shape (4,4)
	array_for_predict = array_for_predict.reshape((1, 4, 3))  # reshape (1,4,4) จะได้ทำนายได้
	print('array_for_predict')
	print(array_for_predict)
	# เอาอาเรย์ไปทำนาย
	# model = tf.keras.models.load_model('bi_4_slide_mape_3_94._Test.h5', compile=False)
	from keras.models import load_model
	model = load_model('bi_4_slide_mape_3_94._Test.h5')
	result_predict = model.predict(array_for_predict,verbose=0)
	# # print("ราคาที่ทำนายได้ของวันที่ " + end_date + " เท่ากับ " + str(result_predic[0][0]))
	num = float(result_predict[-1])
	print(type(num))
	predict = "{:.2f}".format(round(num, 2))
	print(predict)

	return jsonify(predict)


@app.route('/update_data',methods=['GET'])
def update_data():

	import pandas as pd
	import yfinance as yf
	from datetime import datetime

	# ----- รับข้อมูลจากหน้า web ---------
	d = {}
	d['New_Month'] = float(request.args['New_Month'])
	d['Year'] = float(request.args['Year'])
	d['priceThai'] = float(request.args['priceThai'])

	select_date = datetime(int(d['Year'])-543, int(d['New_Month']), 1)
	print('select date')
	print(select_date)
	# df_input = pd.DataFrame([d]) #แปลงเป็น dataframe

	#read excel and find last tail for last date

	df = pd.read_excel('dataofPrice_TrainModel.xlsx')
	df['New_Month'] = pd.to_datetime(df['Date']).dt.strftime('%m').astype('int')
	df['Year'] = pd.to_datetime(df['Date']).dt.strftime('%Y').astype('int')
	print(df)

	# df_result = pd.read_excel('dataofThai.xlsx', index_col=0)
	df_result = df['Thai_Import']
	# df_result = df_result[5:]

	print(df_result)
	print('df_result')
	df_result.to_excel("dataofThai.xlsx", index=False)

	last_day_df = df.tail(1)

	print('last day of')
	print(last_day_df)

	#ทำวันสำหรับใช้ดคงข้อมูล จากวันล่าสุุดของข้อมูลที่มี จนถึงปัจจุบัน
	start_date = datetime(last_day_df['Year'], last_day_df['New_Month'], 1)
	print('start_date')
	print(start_date)

	current_dateTime = datetime.now()
	end_date = datetime(current_dateTime.year, current_dateTime.month, 1)
	print('end_date')
	print(end_date)

	#load Data from yahoo
	data_crude_oil = yf.download(tickers="CL=F", start=start_date, end=end_date, interval='1mo')
	data_crude_oil = data_crude_oil.reset_index()
	data_crude_oil['New_Month'] = pd.to_datetime(data_crude_oil['Date']).dt.strftime('%m').astype('int')
	data_crude_oil['Year'] = pd.to_datetime(data_crude_oil['Date']).dt.strftime('%Y').astype('int')
	data_crude_oil = pd.DataFrame(data_crude_oil, columns=['Date', 'New_Month', 'Year', 'Close'])
	print('data crude oil')
	print(data_crude_oil)

	data_soybean_meal = yf.download(tickers="ZM=F", start=start_date, end=end_date, interval='1mo')
	data_soybean_meal = data_soybean_meal.reset_index()
	data_soybean_meal = pd.DataFrame(data_soybean_meal, columns=['Close'])
	data_soybean_meal = data_soybean_meal.rename(columns={"Close": "Soybean_meal_US"})
	print('data_soybean_meal')
	print(data_soybean_meal)

	#รวมข้อมูลของน้ำมันดิบกับรารากากถั่วเหลือง เลือกเฉพาะ ราคาปิด
	data_thai_import = pd.DataFrame()
	data_thai_import['Thai_Import'] = ['']
	new_data_from_yahoo = pd.DataFrame(data_crude_oil, columns=['Date', 'Thai_Import', 'Close'])
	new_data_from_yahoo = new_data_from_yahoo.rename(columns={"Close": "Crude_Oil"})

	new_data_from_yahoo = new_data_from_yahoo.reset_index(drop=True)
	data_soybean_meal = data_soybean_meal.reset_index(drop=True)
	new_data_from_yahoo = pd.concat([new_data_from_yahoo, data_soybean_meal], axis=1)
	new_data_from_yahoo = new_data_from_yahoo.rename(columns={"Close": "Soybean_meal_US"})
	print('new_data_from_yahoo')
	print(new_data_from_yahoo)

 	#save data above to excel and read
	new_data_from_yahoo.to_excel("new_data_from_yahoo.xlsx", index=False)
	df_from_excel = pd.read_excel('new_data_from_yahoo.xlsx') #soybean_meal_data.xls

	print('df_from_excel')
	print(df_from_excel)
	array_data_load = df_from_excel.to_numpy()

	for i in range(len(array_data_load)):
		for j in range(0, 2):
			if array_data_load[i][j] == select_date:
				print("iffffffffffffffffffffff")
				df_from_excel.loc[[i, i], 'Thai_Import'] = d['priceThai']
				print(i, i)
				print(array_data_load[i][j])

	print('df_from_excel')
	print(df_from_excel)
	df_from_excel.to_excel("new_data_from_yahoo.xlsx",index=False)
	df_from_excel = pd.read_excel('new_data_from_yahoo.xlsx') #soybean_meal_data.xls

	print('read data from excel')
	print(df_from_excel)
	df_from_excel = df_from_excel[['Date', 'Thai_Import', 'Crude_Oil', 'Soybean_meal_US']]
	print(df_from_excel)

	excel_base = pd.read_excel('dataofPrice_TrainModel.xlsx')
	excel_base = excel_base.iloc[:-1]

	print('excel base')

	finaly_df = pd.concat([excel_base, df_from_excel], ignore_index=True, sort=False)
	print(finaly_df.tail(5))


	finaly_df.to_excel("dataofPrice_TrainModel.xlsx", index=False)
	test_excel = pd.read_excel('dataofPrice_TrainModel.xlsx')  # soybean_meal_data.xls
	# test_excel = test_excel[['Date', 'Thai_Import', 'Crude_Oil', 'Soybean_meal_US']]
	print(test_excel)

	slide_month()

	return jsonify(1)

def slide_month():
	# !/usr/bin/env python
	# coding: utf-8

	# In[1]:

	from pandas import read_csv
	import pandas as pd

	# In[2]:

	df = pd.read_excel('dataofPrice_TrainModel.xlsx')  # soybean_meal_data.xls

	# # Date

	# In[3]:

	df_date = df['Date']

	# In[4]:

	array_date = df_date[1:].to_numpy()
	array_date

	# In[5]:

	len(array_date)

	# # thai_import

	# In[6]:

	df_thai = df['Thai_Import']

	# In[7]:

	array_thai = df_thai[:-1].to_numpy()

	# # crude oil

	# In[8]:

	df_crude_oil = df['Crude_Oil']

	# In[9]:

	array_crude_oil = df_crude_oil[1:].to_numpy()

	# # soybeanmealus

	# In[10]:

	df_Soybean_meal_US = df['Soybean_meal_US']

	# In[11]:

	array_Soybean_meal_US = df_Soybean_meal_US[1:].to_numpy()


	# In[14]:

	dataSlideMonth = []
	for i in range(len(array_date)):
		dataSlideMonth.append([])
		for j in range(1):
			dataSlideMonth[i].append(array_date[i])
			dataSlideMonth[i].append(array_thai[i])
			dataSlideMonth[i].append(array_crude_oil[i])
			dataSlideMonth[i].append(array_Soybean_meal_US[i])

	# In[ ]:

	# In[15]:

	compleate_slide_data = pd.DataFrame(dataSlideMonth, columns=['Date', 'Thai_Import', 'Crude_Oil', 'Soybean_meal_US'])

	# In[ ]:

	# In[16]:

	compleate_slide_data.to_excel("compleate_slide_data.xlsx", index=False)
	compleate_slide_data = pd.read_excel('compleate_slide_data.xlsx')
	print('♥♥♥compleate_slide_data♥♥♥')
	print(compleate_slide_data)
	# In[ ]:

	return("slidefinish")


@app.route('/train_model',methods=['GET'])
def train_model():


	from tensorflow.keras.layers import Bidirectional


	import tensorflow as tf
	import pandas as pd

	df = pd.read_excel('compleate_slide_data.xlsx', header=0, index_col=0)
	df

	df_result = pd.read_excel('compleate_slide_data.xlsx')
	df_result = df_result['Thai_Import']
	df_result = df_result[4:]


	df_input_x = df[['Thai_Import', 'Crude_Oil', 'Soybean_meal_US']]
	df_input_y = df_result
	print('df_input_x--------------')
	print(df_input_x)
	print('df_input_y--------------')
	print(df_input_y)


	x_list = df_input_x.values.tolist()
	y_list = df_input_y.values.tolist()


	# univariate lstm example
	from numpy import array
	from keras.models import Sequential
	from keras.layers import LSTM
	from keras.layers import Dense

	# split a univariate sequence into samples
	def split_sequence(sequence, n_steps):
		X = list()
		for i in range(len(sequence)):
			end_ix = i + n_steps
			if end_ix > len(sequence):
				break
			seq_x = sequence[i:end_ix]
			X.append(seq_x)
		return array(X)

	# In[10]:

	n_steps = 4
	x_train = split_sequence(x_list, n_steps)
	len(x_train)



	n_steps = 1
	y_train = split_sequence(y_list, n_steps)
	y_train = y_train.flatten()
	len(y_train)

	# In[13]:

	split_time = 260
	x_train_split = x_train[:split_time]
	y_train_split = y_train[:split_time]

	x_test_split = x_train[split_time:]
	y_test_split = y_train[split_time:]

	n_features = 3


	# define model
	model = Sequential()
	model.add(Bidirectional(LSTM(128, activation='relu', return_sequences=True, ), input_shape=(4, 3)))
	model.add(LSTM(96))
	model.add(Dense(1))
	# model.compile(optimizer='adam', loss='mse')

	# In[90]:

	model.summary()

	# In[91]:

	model.compile(loss='mean_squared_error',
				  optimizer='adam', metrics=[tf.keras.metrics.MeanAbsolutePercentageError(),
											 tf.keras.metrics.MeanAbsoluteError(),
											 tf.keras.metrics.MeanSquaredError()])


	history = model.fit(x_train_split,
						y_train_split,
						batch_size=72,
						epochs=1000,
						validation_data=(x_test_split[:-1], y_test_split),
						shuffle=False)

	# In[108]:

	model.save('bi_4_slide_mape_3_94._Test.h5')

	# In[109]:

	from keras.models import load_model



	model = load_model('bi_4_slide_mape_3_94._Test.h5')

	# In[112]:

	score = model.evaluate(x_test_split[:-1], y_test_split, verbose=0)

	print("Loss is", score[0])
	print("Mean Absolute Percentage Error/ MAPE is", score[1])
	print("Mean Absolute Error/ MAE is", score[2])
	print("Mean Squared Error/ MSE is", score[3])

	return jsonify(1)

@app.route('/excel_value',methods=['GET'])
def read_excelrow():
 	import tensorflow as tf
 	import pandas as pd

 	from keras.models import load_model

 	df = pd.read_excel('dataofPrice_TrainModel.xlsx')

 	df['New_Month'] = pd.to_datetime(df['Date']).dt.strftime('%m').astype('int')
 	df['Year'] = pd.to_datetime(df['Date']).dt.strftime('%Y').astype('int')

 	print(df['New_Month'].iloc[-1])
 	print(df['Year'] .iloc[-1])

 	year_int = int(df['Year'] .iloc[-1]) + 543

 	MONTHS = ["เดือน","มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน", "กรกฎาคม", "สิงหาคม", "กันยายน",
     "ตุลาคม", "พฤศจิกายน", "ธันวาคม"];
 	month = str(MONTHS[df['New_Month'].iloc[-1]])+" "+str(year_int)
 	print((month))
 	return jsonify(month)

if __name__ == '__main__':
	app.run(debug=False)