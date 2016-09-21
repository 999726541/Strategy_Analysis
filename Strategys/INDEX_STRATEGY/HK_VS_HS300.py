from pitcher import MONGODB

#Linear regression example
# This is a very simple example of using two scipy tools
# for linear regression, polyfit and stats.linregress

#Sample data creation
#number of points
#n=50
#t=linspace(-5,5,n)
#print(t)
##parameters
#a=0.8; b=-4
#x=polyval([a,b],t)  # 标准line
##add some noise
#xn=x+randn(n)
#
##Linear regressison -polyfit - polyfit can be used other orders polys
#(ar,br)=polyfit(t,xn,1)
#xr=polyval([ar,br],t)   #新regression line
##compute the mean square error
#err=sqrt(sum((xr-xn)**2)/n)
#
#print('Linear regression using polyfit')
#print('parameters: a=%.2f b=%.2f \nregression: a=%.2f b=%.2f, ms error= %.3f' % (a,b,ar,br,err))
#
##matplotlib ploting
#title('Linear Regression Example')
#plot(t,x,'g.--')
#plot(t,xn,'k.')
#plot(t,xr,'r.-')
#legend(['original','plus noise', 'regression'])
#
#show()
#
##Linear regression using stats.linregress
#(a_s,b_s,r,tt,stderr)=stats.linregress(t,xn)
#print('Linear regression using stats.linregress')
#print('parameters: a=%.2f b=%.2f \nregression: a=%.2f b=%.2f, std error= %.3f' % (a,b,a_s,b_s,stderr))
##hs300 = get_his_data('000300',index=True)
##print(hs300)
#
##nsq = get_data('^HSI',start='2012-01-01',end='2016-09-14')
##print(nsq)
##mango = MONGODB(db='STOCK_INDEX')
##mango.write_to_mongo(nsq,collection='HSI',id='2012-01-01/2016-09-14')

test = MONGODB('STOCK_INDEX')
data = test.read_mongo('NSDAQ',query={'_id':'until/2016-09-14'})
data = data[0]
print(data['Close'])
print(data['Open'])