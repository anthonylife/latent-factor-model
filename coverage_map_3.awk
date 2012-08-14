#!/usr/bin/awk -f
BEGIN{
	FS="\t";
	OFS="\t";
	sum_show=0;  		#记录所有ins的总的show
	index_range = 0;	
	#sample_result是第二轮sign抽样的结果，第一行是Reduce的个数（分桶数），中间是抽样的分界点，最后一行是ins的类型(1普通格式，2列增量，3整合优化，4列增量增和优化)
	while((getline < "sample_result") >0){
		sign_range[index_range] = $1"";		#sign_range存储的是每个分桶的分界点
		index_range = index_range + 1;
	}
	index_range -= 1;
	ins_type=sign_range[index_range]+0;   #ins_type记录输入train_ins的格式，普通、列增量、整合优化、列增量整合优化分别是类别用1、2、3、4表示
	Reduce_num_4=round_04_reduce_num+0;		#Reduce_num_4是第四个hadoop的reduce的个数
	map_partition=ENVIRON["mapred_task_partition"];		#存储当前运行map的编号，用于标注每个ins的lineId；lineId由三个字段处理分别
	Reduce_num_3=index_range-1;		#存储当前运行map的编号，用于标注每个ins的lineId；lineId由三个字段处理分别
														#map编号 map中的顺序(NR) 输入行中的ins号(整合优化每一行有多个ins)
	r_index = 0;		#对每一个输入的行指导一个第四轮处理的reduce桶
	arr_end = index_range-1;		#arr_end是sign_range的数组的最后一个下表值
	sign_range[arr_end] = "999999999999999999999999";		#将最后一个分界点设置为无穷大，第一个设置为0 
	sign_range[0] = "0";
	bucket[0]=0;
	bucket_len=0;
	srand();

	############################
	NF_begin = 2;		#整合优化的第一个非公共部分
	if(1 == ins_type || 3 == ins_type){
		sign_begin = 3; 	#表示用空格分ins后，第一个sign:slot格式的出现位置
		show_begin = 1;		#表示用空格分ins后，show的值所在的位置
	}
	else if(2 == ins_type || 4 == ins_type){
		sign_begin = 4;
		show_begin = 2;
	}
	#########################

	###########################
	#multi_reduce是一个二维数组；存储能被分到第i个reduce的sign也可以允许被分的别的桶；如sign_range数组的内容是[0、3、5、5、7、10]则multi_reduce[0,0]=1 multi_reduce[0,1]=0;multi_reduce[1,0]=2,muli_reduce[1,1]=1,multi_reduce[1,2]=2;第一维表示桶号，第二维的0位表示长度，第二维的第1位表示当前桶号，之后的2-n位表示，可分到当前reduce的sign同时也可以分到别的桶号；程序里只允许分桶边界的sign能够分到多个桶

	for(index_multi=0;index_multi<arr_end;index_multi++){
		multi_reduce[index_multi,1] = index_multi;
		tmp_j = 2;
		large_range = sign_range[index_multi+1];
		for(tmp_i = index_multi+2;tmp_i <= arr_end;tmp_i++){
			if(sign_range[tmp_i] == large_range){
				multi_reduce[index_multi,tmp_j] = tmp_i-1;
				tmp_j++;
			}
			else{
				break;
			}
		}
		multi_reduce[index_multi,tmp_j] = 1;
		multi_reduce[index_multi,0]= tmp_j;
		if(tmp_j > 2){
			index_multi = tmp_i-2;
		}
	}

	#########################
}
function binSearch(bin_sign){                  #折半查找函数，用于查找每个输入sign在抽样结果的哪个范围内，如果sign_range[i]<sign<=sign_range[i+1]则把sign分到i-1的桶里
	bin_begin = 0;
	bin_end = arr_end;
	match_flag = 1;

	while(bin_begin <= bin_end){
		bin_mid = int((bin_begin+bin_end)/2);
		if(sign_range[bin_mid] >= bin_sign && sign_range[bin_mid-1] < bin_sign){
			low = bin_mid-1;
			return low;
		}
		
		if(sign_range[bin_mid] < bin_sign){
			bin_begin = bin_mid+1;
		}
		else{
			bin_end = bin_mid-1;
		}
	}
	return 0;
}
{
	ins_line = $0;		#整个输入行
	tmp_seg1 = $1;		#key
	tmp_value = $1;		#如果是普通格式和列增量格式，$3就是ins
	tmp_weight = $2+0;	#如果是model文件输入，$2是sign的权重
	
	if((NF != 3) || index(ins_line,":")){           #是train_ins的输入行

		r_index = r_index%Reduce_num_4;		#指导第四路分桶，Reduce_num_4是第四轮的reduce，将输入的每一个行指定一个桶
		join_tag = ".";
		tmp_key = r_index""" """map_partition""join_tag""NR;  #生成第四轮map中的key，r_index是指定的桶号,map_partition和NR组成lineId
		r_index++;

		if(1 == ins_type || 2 == ins_type){				#普通格式sign输出,拆分ins
			tmp_key = tmp_key""".0";	#多加的0字段时为了和整合优化格式相同，统一在reduce中的处理方式
			len_sign_slot = split(tmp_value,arr_sign_slot," ");
			show_1 = arr_sign_slot[show_begin]+0;		#show_1记录当前ins的show的值
			for(i=sign_begin; i <= len_sign_slot; i++){		
				split(arr_sign_slot[i],tmp_sign_slot,":");
				#输出字段时key\sign.B\slot\show
				Reduce_index = binSearch(tmp_sign_slot[1]);		#用binSearch函数获取sign的范围 即其分桶号
				if(sign_range[Reduce_index+1] == tmp_sign_slot[1]){	#如果sign是分桶界限的值
					bucket_len = multi_reduce[Reduce_index,0];		#察看其允许被分桶的数目
					multi_reduce[Reduce_index,bucket_len] = multi_reduce[Reduce_index,bucket_len]+1;
					if(multi_reduce[Reduce_index,bucket_len] > bucket_len-1){
						multi_reduce[Reduce_index,bucket_len] = 1;
					}
					tmp_reduce_index = multi_reduce[Reduce_index, multi_reduce[Reduce_index,bucket_len]];	#从这几个桶中随机的选取一个
					print tmp_reduce_index""" """tmp_sign_slot[1]""".B",tmp_sign_slot[2],show_1,tmp_key;
				}
				else{			#如果不是分界的sign，直接输出其改被分的桶
					print Reduce_index""" """tmp_sign_slot[1]""".B",tmp_sign_slot[2],show_1,tmp_key;
				}
			}
			if (4 == sign_begin){
				print r_index""" #.B","##",show_1,int(substr(arr_sign_slot[1],1,10))%Reduce_num_4""" """arr_sign_slot[1]""".0.0"; 
			}
			else{
				sum_show = sum_show + show_1;		#计算总的ins的show
			}
		}
		else if(3 == ins_type || 4 == ins_type){ 	#整合优化格式sign输出,拆分ins
			sub_sum_show_3 = 0;		#记录这个这整合优化的ins的公共部分的show 
			count = 0;
			for(j=NF_begin;j<=NF;j++){	#从第一个非公共部分开始处理
				count = count + 1;		#count用来计数输入的整合优化行中的每个ins的剩余部分，从1开始
				new_key = tmp_key"""."""count;    #对原有的lineId 扩展一个字段，变成Nmap.NR.count用于区分每个ins
				len_sign_slot = split($j,arr_sign_slot," ");
				show_3 = arr_sign_slot[show_begin]+0;		#show_1记录当前ins的show的值
				for(i=sign_begin; i <= len_sign_slot; i++){		
					split(arr_sign_slot[i],tmp_sign_slot,":");
					
					Reduce_index = binSearch(tmp_sign_slot[1]);
					if(sign_range[Reduce_index+1] == tmp_sign_slot[1]){
						bucket_len = multi_reduce[Reduce_index,0];
						multi_reduce[Reduce_index,bucket_len] = multi_reduce[Reduce_index,bucket_len]+1;
						if(multi_reduce[Reduce_index,bucket_len] > bucket_len-1){
							multi_reduce[Reduce_index,bucket_len] = 1;
						}
						tmp_reduce_index = multi_reduce[Reduce_index, multi_reduce[Reduce_index,bucket_len]];	#从这几个桶中随机的选取一个
						print tmp_reduce_index""" """tmp_sign_slot[1]""".B",tmp_sign_slot[2],show_3,new_key;
					}
					else{
						print Reduce_index""" """tmp_sign_slot[1]""".B",tmp_sign_slot[2],show_3,new_key;
					}

				}
				if(4 == sign_begin){
					print r_index""" #.B","##",show_3,int(substr(arr_sign_slot[1],1,10))%Reduce_num_4""" """arr_sign_slot[1]""".0.0"; 
				}
				sub_sum_show_3 += show_3;
			}
			len_sign_slot = split($(NF_begin-1),arr_sign_slot," ");		#每个ins的公共部分拆分
			for(i=sign_begin; i <= len_sign_slot; i++){
				split(arr_sign_slot[i],tmp_sign_slot,":");
				
				Reduce_index = binSearch(tmp_sign_slot[1]);
				if(sign_range[Reduce_index+1] == tmp_sign_slot[1]){
					bucket_len = multi_reduce[Reduce_index,0];
					multi_reduce[Reduce_index,bucket_len] = multi_reduce[Reduce_index,bucket_len]+1;
					if(multi_reduce[Reduce_index,bucket_len] > bucket_len-1){
						multi_reduce[Reduce_index,bucket_len] = 1;
					}
					tmp_reduce_index = multi_reduce[Reduce_index, multi_reduce[Reduce_index,bucket_len]];	#从这几个桶中随机的选取一个
					print tmp_reduce_index""" """tmp_sign_slot[1]""".B",tmp_sign_slot[2],sub_sum_show_3,tmp_key""".0";
				}
				else{
					print Reduce_index""" """tmp_sign_slot[1]""".B",tmp_sign_slot[2],sub_sum_show_3,tmp_key""".0";
				}

			}
			if(3 == sign_begin){
				sum_show = sum_show + sub_sum_show_3;	#计算总的ins的show
			}
		}
	}
	else{		#如果是model文件中的输入行，过滤weight后输出里面的第一字段sign
		if(tmp_weight > 0.001 || tmp_weight < -0.001){
			Reduce_index = binSearch(tmp_seg1);
			if(sign_range[Reduce_index+1] == tmp_seg1){	#对于model里允许分到多个桶的sign，保证每个桶都有这个sign的输入
				bucket_len = multi_reduce[Reduce_index,0];
				for(i=1;i<=bucket_len;i++){
					tmp_reduce_index = multi_reduce[Reduce_index,i];
					print tmp_reduce_index""" """tmp_seg1""".A";
				}
			}
			else{
				print Reduce_index""" """tmp_seg1""".A";
			}
		}
	}
}
END{
	if(3 == sign_begin){
		print "0 #.B","##",sum_show,"0 """map_partition""".0.0";
		print "0 #.A";
	}
	else if("0" == map_partition){	#在第0个map中,为每个Reduce输出一个 #.A 避免漏掉每行ins的show的加和
		for(tmp_map = 0; tmp_map < Reduce_num_3; tmp_map++){
			print tmp_map""" #.A";
		}
	}
}
