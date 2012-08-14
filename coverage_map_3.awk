#!/usr/bin/awk -f
BEGIN{
	FS="\t";
	OFS="\t";
	sum_show=0;  		#��¼����ins���ܵ�show
	index_range = 0;	
	#sample_result�ǵڶ���sign�����Ľ������һ����Reduce�ĸ�������Ͱ�������м��ǳ����ķֽ�㣬���һ����ins������(1��ͨ��ʽ��2��������3�����Ż���4�����������Ż�)
	while((getline < "sample_result") >0){
		sign_range[index_range] = $1"";		#sign_range�洢����ÿ����Ͱ�ķֽ��
		index_range = index_range + 1;
	}
	index_range -= 1;
	ins_type=sign_range[index_range]+0;   #ins_type��¼����train_ins�ĸ�ʽ����ͨ���������������Ż��������������Ż��ֱ��������1��2��3��4��ʾ
	Reduce_num_4=round_04_reduce_num+0;		#Reduce_num_4�ǵ��ĸ�hadoop��reduce�ĸ���
	map_partition=ENVIRON["mapred_task_partition"];		#�洢��ǰ����map�ı�ţ����ڱ�עÿ��ins��lineId��lineId�������ֶδ���ֱ�
	Reduce_num_3=index_range-1;		#�洢��ǰ����map�ı�ţ����ڱ�עÿ��ins��lineId��lineId�������ֶδ���ֱ�
														#map��� map�е�˳��(NR) �������е�ins��(�����Ż�ÿһ���ж��ins)
	r_index = 0;		#��ÿһ���������ָ��һ�������ִ����reduceͰ
	arr_end = index_range-1;		#arr_end��sign_range����������һ���±�ֵ
	sign_range[arr_end] = "999999999999999999999999";		#�����һ���ֽ������Ϊ����󣬵�һ������Ϊ0 
	sign_range[0] = "0";
	bucket[0]=0;
	bucket_len=0;
	srand();

	############################
	NF_begin = 2;		#�����Ż��ĵ�һ���ǹ�������
	if(1 == ins_type || 3 == ins_type){
		sign_begin = 3; 	#��ʾ�ÿո��ins�󣬵�һ��sign:slot��ʽ�ĳ���λ��
		show_begin = 1;		#��ʾ�ÿո��ins��show��ֵ���ڵ�λ��
	}
	else if(2 == ins_type || 4 == ins_type){
		sign_begin = 4;
		show_begin = 2;
	}
	#########################

	###########################
	#multi_reduce��һ����ά���飻�洢�ܱ��ֵ���i��reduce��signҲ���������ֵı��Ͱ����sign_range�����������[0��3��5��5��7��10]��multi_reduce[0,0]=1 multi_reduce[0,1]=0;multi_reduce[1,0]=2,muli_reduce[1,1]=1,multi_reduce[1,2]=2;��һά��ʾͰ�ţ��ڶ�ά��0λ��ʾ���ȣ��ڶ�ά�ĵ�1λ��ʾ��ǰͰ�ţ�֮���2-nλ��ʾ���ɷֵ���ǰreduce��signͬʱҲ���Էֵ����Ͱ�ţ�������ֻ�����Ͱ�߽��sign�ܹ��ֵ����Ͱ

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
function binSearch(bin_sign){                  #�۰���Һ��������ڲ���ÿ������sign�ڳ���������ĸ���Χ�ڣ����sign_range[i]<sign<=sign_range[i+1]���sign�ֵ�i-1��Ͱ��
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
	ins_line = $0;		#����������
	tmp_seg1 = $1;		#key
	tmp_value = $1;		#�������ͨ��ʽ����������ʽ��$3����ins
	tmp_weight = $2+0;	#�����model�ļ����룬$2��sign��Ȩ��
	
	if((NF != 3) || index(ins_line,":")){           #��train_ins��������

		r_index = r_index%Reduce_num_4;		#ָ������·��Ͱ��Reduce_num_4�ǵ����ֵ�reduce���������ÿһ����ָ��һ��Ͱ
		join_tag = ".";
		tmp_key = r_index""" """map_partition""join_tag""NR;  #���ɵ�����map�е�key��r_index��ָ����Ͱ��,map_partition��NR���lineId
		r_index++;

		if(1 == ins_type || 2 == ins_type){				#��ͨ��ʽsign���,���ins
			tmp_key = tmp_key""".0";	#��ӵ�0�ֶ�ʱΪ�˺������Ż���ʽ��ͬ��ͳһ��reduce�еĴ���ʽ
			len_sign_slot = split(tmp_value,arr_sign_slot," ");
			show_1 = arr_sign_slot[show_begin]+0;		#show_1��¼��ǰins��show��ֵ
			for(i=sign_begin; i <= len_sign_slot; i++){		
				split(arr_sign_slot[i],tmp_sign_slot,":");
				#����ֶ�ʱkey\sign.B\slot\show
				Reduce_index = binSearch(tmp_sign_slot[1]);		#��binSearch������ȡsign�ķ�Χ �����Ͱ��
				if(sign_range[Reduce_index+1] == tmp_sign_slot[1]){	#���sign�Ƿ�Ͱ���޵�ֵ
					bucket_len = multi_reduce[Reduce_index,0];		#�쿴��������Ͱ����Ŀ
					multi_reduce[Reduce_index,bucket_len] = multi_reduce[Reduce_index,bucket_len]+1;
					if(multi_reduce[Reduce_index,bucket_len] > bucket_len-1){
						multi_reduce[Reduce_index,bucket_len] = 1;
					}
					tmp_reduce_index = multi_reduce[Reduce_index, multi_reduce[Reduce_index,bucket_len]];	#���⼸��Ͱ�������ѡȡһ��
					print tmp_reduce_index""" """tmp_sign_slot[1]""".B",tmp_sign_slot[2],show_1,tmp_key;
				}
				else{			#������Ƿֽ��sign��ֱ�������ı��ֵ�Ͱ
					print Reduce_index""" """tmp_sign_slot[1]""".B",tmp_sign_slot[2],show_1,tmp_key;
				}
			}
			if (4 == sign_begin){
				print r_index""" #.B","##",show_1,int(substr(arr_sign_slot[1],1,10))%Reduce_num_4""" """arr_sign_slot[1]""".0.0"; 
			}
			else{
				sum_show = sum_show + show_1;		#�����ܵ�ins��show
			}
		}
		else if(3 == ins_type || 4 == ins_type){ 	#�����Ż���ʽsign���,���ins
			sub_sum_show_3 = 0;		#��¼����������Ż���ins�Ĺ������ֵ�show 
			count = 0;
			for(j=NF_begin;j<=NF;j++){	#�ӵ�һ���ǹ������ֿ�ʼ����
				count = count + 1;		#count������������������Ż����е�ÿ��ins��ʣ�ಿ�֣���1��ʼ
				new_key = tmp_key"""."""count;    #��ԭ�е�lineId ��չһ���ֶΣ����Nmap.NR.count��������ÿ��ins
				len_sign_slot = split($j,arr_sign_slot," ");
				show_3 = arr_sign_slot[show_begin]+0;		#show_1��¼��ǰins��show��ֵ
				for(i=sign_begin; i <= len_sign_slot; i++){		
					split(arr_sign_slot[i],tmp_sign_slot,":");
					
					Reduce_index = binSearch(tmp_sign_slot[1]);
					if(sign_range[Reduce_index+1] == tmp_sign_slot[1]){
						bucket_len = multi_reduce[Reduce_index,0];
						multi_reduce[Reduce_index,bucket_len] = multi_reduce[Reduce_index,bucket_len]+1;
						if(multi_reduce[Reduce_index,bucket_len] > bucket_len-1){
							multi_reduce[Reduce_index,bucket_len] = 1;
						}
						tmp_reduce_index = multi_reduce[Reduce_index, multi_reduce[Reduce_index,bucket_len]];	#���⼸��Ͱ�������ѡȡһ��
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
			len_sign_slot = split($(NF_begin-1),arr_sign_slot," ");		#ÿ��ins�Ĺ������ֲ��
			for(i=sign_begin; i <= len_sign_slot; i++){
				split(arr_sign_slot[i],tmp_sign_slot,":");
				
				Reduce_index = binSearch(tmp_sign_slot[1]);
				if(sign_range[Reduce_index+1] == tmp_sign_slot[1]){
					bucket_len = multi_reduce[Reduce_index,0];
					multi_reduce[Reduce_index,bucket_len] = multi_reduce[Reduce_index,bucket_len]+1;
					if(multi_reduce[Reduce_index,bucket_len] > bucket_len-1){
						multi_reduce[Reduce_index,bucket_len] = 1;
					}
					tmp_reduce_index = multi_reduce[Reduce_index, multi_reduce[Reduce_index,bucket_len]];	#���⼸��Ͱ�������ѡȡһ��
					print tmp_reduce_index""" """tmp_sign_slot[1]""".B",tmp_sign_slot[2],sub_sum_show_3,tmp_key""".0";
				}
				else{
					print Reduce_index""" """tmp_sign_slot[1]""".B",tmp_sign_slot[2],sub_sum_show_3,tmp_key""".0";
				}

			}
			if(3 == sign_begin){
				sum_show = sum_show + sub_sum_show_3;	#�����ܵ�ins��show
			}
		}
	}
	else{		#�����model�ļ��е������У�����weight���������ĵ�һ�ֶ�sign
		if(tmp_weight > 0.001 || tmp_weight < -0.001){
			Reduce_index = binSearch(tmp_seg1);
			if(sign_range[Reduce_index+1] == tmp_seg1){	#����model������ֵ����Ͱ��sign����֤ÿ��Ͱ�������sign������
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
	else if("0" == map_partition){	#�ڵ�0��map��,Ϊÿ��Reduce���һ�� #.A ����©��ÿ��ins��show�ļӺ�
		for(tmp_map = 0; tmp_map < Reduce_num_3; tmp_map++){
			print tmp_map""" #.A";
		}
	}
}
